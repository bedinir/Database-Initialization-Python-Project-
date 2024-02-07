import sqlite3
import json

# Opening JSON file
with open('csvjson.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

print(json_object)
# print(type(json_object))

# Connect to SQLite database (create a new one if not exists)
db_name = 'demographic.db'  # Replace with your desired database name
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create Region table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Region (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

# Create Education table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT NOT NULL
    )
''')

# Create Employment table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL
    )
''')

# Create demographic_data table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Demographic_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER,
        education_id INTEGER,
        employment_id INTEGER,
        age INTEGER,
        income INTEGER,
        FOREIGN KEY (region_id) REFERENCES Region(id),
        FOREIGN KEY (education_id) REFERENCES Education(id),
        FOREIGN KEY (employment_id) REFERENCES Employment(id)
    )
''')

# Commit changes to the database
conn.commit()

# Function to check if region exists in the Region table
def row_exists(table_name, column_name, column_value):
    query = f'SELECT 1 FROM {table_name} WHERE {column_name}=?'
    cursor.execute(query, (column_value,))
    return cursor.fetchone() is not None

# Insert data into Region, Education, and Employment tables
for entry in json_object:
    region_name = entry.get('Region', '')
    education_level = entry.get('Education', '')
    employment_status = entry.get('Employment', '')
    age = entry.get('Age', None)
    income = entry.get('Income', None)
    
    # Insert into Region table
    if not row_exists('Region','name',region_name):
        cursor.execute('INSERT INTO Region (name) VALUES (?)', (region_name,))

    # Insert into Education table
    if not row_exists('Education','level',education_level):
        cursor.execute('INSERT INTO Education (level) VALUES (?)', (education_level,))

    # Insert into Employment table
    if not row_exists('Employment','status',employment_status):
        cursor.execute('INSERT INTO Employment (status) VALUES (?)', (employment_status,))

     # Get IDs for Region, Education, and Employment
    region_id = cursor.execute('SELECT id FROM Region WHERE name=?', (region_name,)).fetchone()[0]
    education_id = cursor.execute('SELECT id FROM Education WHERE level=?', (education_level,)).fetchone()[0]
    employment_id = cursor.execute('SELECT id FROM Employment WHERE status=?', (employment_status,)).fetchone()[0]

    # Insert into demographic_data table if not exists
    if (
        region_name and education_level and employment_status and age is not None and income is not None
        # and not row_exists('demographic_data', 'region_id', region_id)
        # and not row_exists('demographic_data', 'education_id', education_id)
        # and not row_exists('demographic_data', 'employment_id', employment_id)
    ):
        cursor.execute('INSERT INTO demographic_data (region_id, education_id, employment_id, age, income) VALUES (?, ?, ?, ?, ?)',
                       (region_id, education_id, employment_id, age, income))
# Commit changes to the database
conn.commit()

# Close the connection
conn.close()