import uuid

from sqlalchemy import Column, DateTime, Float, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database import BaseORM


class RidersORM(BaseORM):
    __tablename__ = 'riders'

    rider_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)


class OrdersORM(BaseORM):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pick_up_time = Column(DateTime(timezone=True))
    delivery_time = Column(DateTime(timezone=True))
    distance = Column(Float)
    rider_name = Column(String)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    directions = Column(Integer)


class RestaurantsORM(BaseORM):
    __tablename__ = 'restaurants'

    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_name = Column(String)
    restaurant_coord = Column(String)
    restaurant_lat = Column(Float)
    restaurant_lng = Column(Float)


class CustomersORM(BaseORM):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String)
    customer_coord = Column(String)
    customer_lat = Column(Float)
    customer_lng = Column(Float)
