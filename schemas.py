from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Directions(str, Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class Rider(BaseModel):
    rider_id: str
    name: str
    current_location: Optional[str] = "C4"
    in_service: Optional[str]

    class Config:
        orm_mode = True


class Customer(BaseModel):
    customer_id: int
    customer_name: str
    customer_coord: str
    customer_lat: float
    customer_lng: float

    class Config:
        orm_mode = True


class Restaurant(BaseModel):
    restaurant_id: int
    restaurant_name: str
    restaurant_coord: str
    restaurant_lat: float
    restaurant_lng: float

    class Config:
        orm_mode = True


class Order(BaseModel):
    order_id: str
    ordered_at: str
    order_value: float
    restaurant_id: int
    customer_id: int


class DeliveredOrder(BaseModel):
    order_id: Optional[str]
    pick_up_time: Optional[datetime]
    delivery_time: Optional[datetime]
    distance : int
    rider_name: str
    restaurant_id: int
    customer_id: int
    directions: str

    class Config:
        orm_mode = True
