
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Order, Package, Sender,Courier,Address,Receiver,ServiceType, OrderDelivery, CourierOrderDelivery, History
from utils import *

# Load data from JSON file
with open('delivery_system.json', 'r') as f:
    data = json.load(f)

# Create SQLAlchemy engine
engine = create_engine('sqlite:///delivery_management.db')

# Create session
Session = sessionmaker(bind=engine)
session = Session()

for order_data in data:

  #Receiver
   address= create_address(order_data['receiver'])
   session.add(address)
   session.flush()

   receiver = create_receiver(order_data['receiver'], address.id)
   session.add(receiver)
   session.flush()

  #Sender
   sender = session.query(Sender).filter_by(id=order_data['sender']['id']).first()

   if sender is None:
     address= create_address(order_data['sender'])
     session.add(address)
     session.flush()
     sender = create_sender(order_data['sender'], address.id)
     session.add(sender)
     session.flush()

   #Package
   package = create_package(order_data['package'])
   session.add(package)
   session.flush()

   #Order
   order = create_order(order_data)
   order.receiver_id =receiver.id
   order.sender_id =sender.id
   order.package_id =package.id

   session.add(order)
   session.flush()

   #Service Type
   service_type_name = order_data['serviceType']
   service_type = session.query(ServiceType).filter_by(name=service_type_name).first()

   if not service_type:
        service_type = create_serviceType(service_type_name)
        session.add(service_type)
        session.flush()

   #Order Delivery
   order_delivery = create_order_delivery(order_data['servicePrice'], service_type,order.id)
   session.add(order_delivery)
   session.flush()

   #Couriers
   for courier_data in order_data['couriers']:
    courier = session.query(Courier).filter_by(id=courier_data['id']).first()
    if courier is None:
       courier = create_courier(courier_data)
       session.add(courier)
       session.flush()

    courier_order_delivery =create_courier_order_delivery(courier_data['plate'], courier.id, order_delivery.id)
    session.add(courier_order_delivery)
    session.flush()

   #History
   for history_data in order_data['history']:
       history =create_history(history_data)
       history.order_id= order.id
       session.add(history)
       session.flush()

# Commit the transaction to save the data
session.commit()

# Close session
session.close()