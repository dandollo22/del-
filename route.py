from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette import status

from database import SessionLocal
from exceptions import NoAvailableRiders
from helper import DeliveryHelper
from schemas import Order
from service import DeliveryService

delivery_helper = DeliveryHelper(SessionLocal)
delivery_service = DeliveryService(delivery_helper)

delivery_route = APIRouter(tags=['hour-rush'])


@delivery_route.put("/new-oder")
def create_new_order(order: Order):
    """Insert a new order in the orders table"""
    try:
        return delivery_service.deliver_order(order)
    except NoAvailableRiders as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There are no available riders currently") from e