## Database Initialization (Python Project)

If you prefer to initialize the database using a Python script, you can use the following project to achieve that:

### Project Overview

The Python project consists of several files to initialize the database from a JSON file, insert data into the database, and define utility functions.

### Project Structure

The project is structured as follows:

 - db_schema.py # Python script defining the database schema
 - delivery_system.json # JSON file containing data for database initialization
 - insert_data.py # Python script to insert data into the database
 - utils.py # Python script containing utility functions
 - README.md # Project documentation


### Usage

1. Ensure you have Python installed on your system.
2. Clone the repository or download the project files.
3. Navigate to the project directory in your terminal.
4. Run the `db_schema.py` script to define the database schema:
    ```
    python db_schema.py
    ```
5. Run the `insert_data.py` script to insert data into the database:
    ```
    python insert_data.py
    ```
6. The database will be created based on the schema defined in `db_schema.py`, and data will be inserted from the `delivery_system.json` file.
