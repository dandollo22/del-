import uuid

from sqlalchemy import Column, DateTime, Float, String, Integer, ForeignKey, Boolean

from database import BaseORM


class RidersORM(BaseORM):
    __tablename__ = 'riders'

    rider_id = Column(String, primary_key=True)
    name = Column(String)
    current_location = Column(String)
    working = Column(Boolean, default=True)
    in_service = Column(String, ForeignKey("orders.order_id"), nullable=True)


class OrdersORM(BaseORM):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, default=str(uuid.uuid4))
    pick_up_time = Column(DateTime(timezone=True))
    delivery_time = Column(DateTime(timezone=True))
    distance = Column(Integer)
    rider_name = Column(String)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    directions = Column(String)


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
