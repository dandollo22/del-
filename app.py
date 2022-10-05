from pprint import pprint

import pydantic
import uvicorn
from fastapi import FastAPI

from database import BaseORM, engine
from route import delivery_route, delivery_helper, delivery_service
from schemas import Order, Rider, Restaurant, Customer


def create_database():
    return BaseORM.metadata.create_all(bind=engine)


def save_data_to_db():
    customers = pydantic.parse_file_as(path='data/customers.json', type_=list[Customer])
    orders = pydantic.parse_file_as(path='data/orders.json', type_=list[Order])
    restaurants = pydantic.parse_file_as(path='data/restaurants.json', type_=list[Restaurant])
    riders = pydantic.parse_file_as(path='data/riders.json', type_=list[Rider])

    delivery_helper.insert_restaurants(restaurants)
    delivery_helper.insert_riders(riders)
    delivery_helper.insert_customers(customers)

    submitted_orders = [delivery_service.deliver_order(order).dict() for order in orders]
    pprint(submitted_orders)


app = FastAPI(title="Delivering API")
app.include_router(delivery_route)

if __name__ == "__main__":
    create_database()
    save_data_to_db()

    uvicorn.run(app=app)
