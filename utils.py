# Add needed functions to use in the insert_data.py

from datetime import datetime
import uuid
from db_schema import Order, Package, Sender, Courier, Address, Receiver, ServiceType, OrderDelivery, CourierOrderDelivery, History, CurrencyTypeEnum, PackageTypeEnum, OrderStatusEnum

def create_order(data):
        order = Order(
        id=data['id'],
        code=data['code'],
        created_date=datetime.strptime(data['createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date(),
        status= get_enum_value(OrderStatusEnum, data['status'], default=OrderStatusEnum.created),
        ) 
        return order

def create_package(data):
        package = Package(
        id=data['id'],
        weight=int(data['weight']), 
        package_type= get_enum_value(PackageTypeEnum, data['package_type'], default=PackageTypeEnum.package),
        value=float(data['value']),
        currency=get_enum_value(CurrencyTypeEnum, data['currency'], default=CurrencyTypeEnum.euro),
        )
        return package

def create_courier(data):
        courier = Courier(
        id=data['id'],
        email=data['email'], 
        username=data['username'].split('@')[0],
        phoneNumber=data['phoneNumber'],
        )
        return courier

def create_history(data):
        history = History(
        id=data['id'],
        date=datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%fZ').date(),
        status=get_enum_value(OrderStatusEnum, data['status'], default=OrderStatusEnum.created),
        note=data['note'],
        )
        return history

def create_sender(data, addressId):
        sender = Sender(
        id=data['id'],
        email=data['email'], 
        username=data['username'].split('@')[0],
        address_id=addressId
        )
        return sender

def create_receiver(data, addressId):
        receiver = Receiver(
        id=data['id'],
        name=data['name'],
        address_id=addressId
        )
        return receiver
    
def create_address(data):
       address = Address(
        id=str(uuid.uuid4()),
        country=data['country'],
        city=data['city'],
        street=data['street'],
        phoneNumber=data['phoneNumber']
        )
       return address

def create_serviceType(service_type_name):
        serviceType = ServiceType(
        id=str(uuid.uuid4()),
        name=service_type_name
        )
        return serviceType
 
def create_order_delivery(service_price, service_type, order_id):
        orderDelivery = OrderDelivery(
        id=str(uuid.uuid4()),
        servicePrice=float(service_price),
        service_type_id=service_type.id,
        order_id =order_id
        )
        return orderDelivery

def create_courier_order_delivery(plate, courier_id, order_delivery_id):
        courierOrderDelivery = CourierOrderDelivery(
        id=str(uuid.uuid4()),
        plate=plate,
        courier_id=courier_id,
        order_delivery_id =order_delivery_id
        )
        return courierOrderDelivery

def get_enum_value(enum_class, value_str, default=None):
      for enum_value in enum_class:
        if enum_value.value == value_str:
            return enum_value

      return default