import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Order, Package, User, Sender,Courier,Address,Receiver,ServiceType, OrderDelivery, CourierOrderDelivery, History
from utils import *

# Load data from JSON file
with open('delivery_system.json', 'r') as f:
    data = json.load(f)

# Create SQLAlchemy engine
engine = create_engine('sqlite:///delivery_management.db')

# Create session
Session = sessionmaker(bind=engine)
session = Session()


































# Commit the transaction to save the data
session.commit()

# Close session
session.close()