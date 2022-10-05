from datetime import datetime

import sqlalchemy.sql.functions
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from models import RestaurantsORM, CustomersORM, OrdersORM, RidersORM
from schemas import Restaurant, Customer, DeliveredOrder, Rider


class DeliveryHelper:
    def __init__(self, session_maker: sessionmaker):
        self._session_maker = session_maker

    def get_restaurant(self, restaurant_id: int) -> Restaurant:
        """Get the restaurant by id"""
        with self._session_maker(expire_on_commit=False) as session:
            query = session.query(RestaurantsORM).filter(RestaurantsORM.restaurant_id == restaurant_id).first()
        return Restaurant.from_orm(query)

    def get_customer(self, customer_id: int) -> Customer:
        """Get customer by id"""
        with self._session_maker(expire_on_commit=False) as session:
            query = session.query(CustomersORM).filter(CustomersORM.customer_id == customer_id).first()
        return Customer.from_orm(query)

    def get_list_riders(self) -> list[Rider]:
        """get the list of available riders"""
        with self._session_maker(expire_on_commit=False) as session:
            query = session.query(RidersORM).filter(RidersORM.in_service == None, RidersORM.working == True).all()
        return [Rider.from_orm(rider) for rider in query]

    def get_next_available_rider(self) -> tuple[Rider, datetime]:
        """get the rider which is going to be available the soonest"""
        with self._session_maker(expire_on_commit=False) as session:
            rider, next_available = session.query(RidersORM, OrdersORM.delivery_time).join(OrdersORM).order_by(
                sqlalchemy.asc(OrdersORM.delivery_time)).first()
            rider = Rider.from_orm(rider) if rider else None
        return rider, next_available

    def save_oder(self, order: DeliveredOrder) -> DeliveredOrder:
        """Save an order details"""
        with self._session_maker(expire_on_commit=False) as session:
            new_order = OrdersORM(**order.dict())
            session.add(new_order)
            try:
                session.commit()
                session.refresh(new_order)
            except IntegrityError:
                session.rollback()

            return DeliveredOrder.from_orm(new_order)

    def set_rider_order(self, rider: Rider, order_id: str) -> Rider:
        """Set the rider for a specific order"""
        with self._session_maker(expire_on_commit=False) as session:
            rider = session.query(RidersORM).filter(RidersORM.rider_id == rider.rider_id).first()
            rider.in_service = order_id
            session.commit()
            session.refresh(rider)
            return Rider.from_orm(rider)

    def insert_restaurants(self, restaurants: list[Restaurant]):
        """Insert a list of restaurants"""
        with self._session_maker(expire_on_commit=False) as session:
            for restaurant in restaurants:
                session.add(RestaurantsORM(**restaurant.dict()))
            try:
                session.commit()
            except IntegrityError:
                session.rollback()

    def insert_customers(self, customers: list[Customer]):
        """Insert a list of customer"""
        with self._session_maker(expire_on_commit=False) as session:
            for customer in customers:
                session.add(CustomersORM(**customer.dict()))
            try:
                session.commit()
            except IntegrityError:
                session.rollback()

    def insert_riders(self, riders: list[Rider]):
        """Insert a list of riders"""
        with self._session_maker(expire_on_commit=False) as session:
            for rider in riders:
                session.add(RidersORM(**rider.dict(exclude_none=True)))
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
