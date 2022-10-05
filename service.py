from datetime import datetime, timedelta

import geopy.distance

from exceptions import NoAvailableRiders
from helper import DeliveryHelper
from schemas import Rider, Order, DeliveredOrder, Directions, Restaurant


class DeliveryService:
    RIDERS_SPEED = 1

    def __init__(self, helper: DeliveryHelper):
        self.helper = helper

    @staticmethod
    def _compute_direction(rider_location: str, targeted_location: str) -> str:
        """Get the direction to take from a start position into a target location"""
        direction = ""
        lateral, vertical = (
            ord(rider_location[0]) - ord(targeted_location[0]),
            ord(rider_location[1]) - ord(targeted_location[1]),
        )
        if lateral:
            direction += (abs(lateral) + 1) * Directions.EAST if lateral < 0 else (abs(lateral)) * Directions.WEST
        if vertical:
            direction += (abs(vertical) + 1) * Directions.SOUTH if vertical < 0 else (abs(vertical)) * Directions.NORTH

        return direction

    @staticmethod
    def _closest_rider(list_riders: list[Rider], target_location: str) -> Rider:
        """find the closest rider for a specific target location"""

        def _calculate_distance(x):
            return (
                           (ord(x.current_location[0]) - ord(target_location[0])) ** 2
                           + (ord(x.current_location[0]) - ord(target_location[0])) ** 2
                   ) ** 0.5

        riders = {_calculate_distance(rider): rider for rider in list_riders}
        return riders[min(riders.keys())]

    @staticmethod
    def _calculate_distance(coords_1: tuple[float, float], coords_2: tuple[float, float]) -> float:
        """calculate the distance"""
        return geopy.distance.geodesic(coords_1, coords_2).meters

    def get_rider(self, restaurant_coord: str) -> tuple[Rider, datetime]:
        """Choose the best fit rider for a specific restaurant delivery"""
        wait_time = None
        if list_riders := self.helper.get_list_riders():
            deliver_rider = self._closest_rider(list_riders, restaurant_coord)

        else:
            deliver_rider, wait_time = self.helper.get_next_available_rider()

        if not deliver_rider:
            raise NoAvailableRiders

        return deliver_rider, wait_time

    @staticmethod
    def compute_pick_up_time(next_available, rider: Rider = None, restaurant: Restaurant = None):
        """Calculate the pick-up time of a delivery"""
        # Todo:to be extended to consider the time needed for the rider to get from current location to restaurant
        #  location
        default_next_available = datetime.now()
        return next_available or default_next_available

    def deliver_order(self, order: Order) -> DeliveredOrder:
        """Compute the response for a deliverable order """
        restaurant = self.helper.get_restaurant(order.restaurant_id)
        customer = self.helper.get_customer(order.customer_id)

        deliver_rider, next_available = self.get_rider(restaurant.restaurant_coord)

        directions = self._compute_direction(restaurant.restaurant_coord, customer.customer_coord)
        distance = self._calculate_distance((restaurant.restaurant_lat, restaurant.restaurant_lng),
                                            (customer.customer_lat, customer.customer_lng))
        pick_up_time = self.compute_pick_up_time(next_available)
        created_order = DeliveredOrder(
            directions=directions,
            rider_name=deliver_rider.name,
            order_id=order.order_id,
            customer_id=customer.customer_id,
            restaurant_id=restaurant.restaurant_id,
            distance=distance,
            pick_up_time=pick_up_time,
            delivery_time=pick_up_time + timedelta(minutes=distance * self.RIDERS_SPEED)

        )
        order = self.helper.save_oder(created_order)
        self.helper.set_rider_order(deliver_rider, order.order_id)

        return order
