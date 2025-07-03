"""Travel Master.

This module defines a comprehensive AI Travel Master system.
It includes specialized assistants for Flight, Accommodation, and Car Rental services, 
coordinated by a travel master supervisor.
"""

from travel_master.flight_assistant.flight_assistant import graph as flight_assistant
from travel_master.accommodation_assistant.accommodation_assistant import (
    graph as accommodation_assistant,
)
from travel_master.car_rental_assistant.car_rental_assistant import graph as car_rental_assistant
from travel_master.travel_master import graph as travel_master

__all__ = ["flight_assistant", "accommodation_assistant", "car_rental_assistant", "travel_master"]
