# Import the necessary libraries
import enum
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum, Date, ForeignKeyConstraint
from sqlalchemy.orm  import declarative_base

# Create an engine to connect to the database
engine = create_engine('sqlite:///delivery_management.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

#Enums 
class OrderStatusEnum(enum.Enum):
    pickup= 'pick-up'
    created='created'
    accepted='accepted'
    tranzit='tranzit'
    rejected = 'rejected'
    delivered = 'delivered'
    distribution = 'for-distribution'

class PackageTypeEnum(enum.Enum):
    package= 'package'
    document = 'document'

class CurrencyTypeEnum(enum.Enum):
    dollar= 'dollar'
    euro = 'euro'
 

# classes
class Order(Base):
    __tablename__ = 'orders'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    code = Column(String)
    status = Column(Enum(OrderStatusEnum))
    created_date = Column(Date)

    receiver_id = Column(String, ForeignKey('receivers.id'))
    sender_id = Column(String, ForeignKey('senders.id'))
    package_id = Column(String, ForeignKey('packages.id'))

class Package(Base):
    __tablename__ = 'packages'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    weight = Column(Integer)
    package_type = Column(Enum(PackageTypeEnum))
    currency = Column(Enum(CurrencyTypeEnum))
    value = Column(Float)


class Sender(Base):
    __tablename__ = 'senders'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    email = Column(String)
    username = Column(String)

    address_id = Column(String, ForeignKey('addresses.id'))

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    country = Column(String)
    city = Column(String)
    street = Column(String)
    phoneNumber = Column(String)


class Receiver(Base):
    __tablename__ = 'receivers'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String)

    address_id = Column(String, ForeignKey('addresses.id'))

class ServiceType(Base):
    __tablename__ = 'service_types'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String)

class Courier(Base):
    __tablename__ = 'couriers'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    phoneNumber = Column(String)
    email = Column(String)
    username = Column(String)

class OrderDelivery(Base):
    __tablename__ = 'order_deliveries'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    servicePrice = Column(Float)

    service_type_id = Column(String, ForeignKey('service_types.id'))
    order_id = Column(String, ForeignKey('orders.id'))

class CourierOrderDelivery(Base):
    __tablename__ = 'courier_order_deliveries'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    plate = Column(String)

    courier_id = Column(String, ForeignKey('couriers.id'))
    order_delivery_id = Column(String, ForeignKey('order_deliveries.id'))


class History(Base):
    __tablename__ = 'histories'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    date = Column(Date)
    status = Column(Enum(OrderStatusEnum))
    note = Column(String)
    order_id = Column(String, ForeignKey('orders.id'))

# Define foreign key constraints
ForeignKeyConstraint(['receiver_id'], ['receivers.id']),
ForeignKeyConstraint(['sender_id'], ['senders.id']),
ForeignKeyConstraint(['order_delivery_id'], ['order_deliveries.id']),
ForeignKeyConstraint(['package_id'], ['packages.id']),
ForeignKeyConstraint(['address_id'], ['addresses.id'])


# Create the table
Base.metadata.create_all(engine)