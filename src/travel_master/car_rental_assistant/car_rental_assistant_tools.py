"""Tools for the Car Rental assistant."""

import json
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, cast
import random

import aiohttp
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from travel_master.configuration import Configuration


async def search_cars(
    location: str,
    pickup_date: str,
    dropoff_date: str,
    pickup_time: str = "10:00",
    dropoff_time: str = "10:00",
    car_type: str = "economy",
    age: int = 25,
    *,
    config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, Any]:
    """Search for car rentals using real web search.

    Args:
        location: Pickup location (city, airport, etc.)
        pickup_date: Pickup date (YYYY-MM-DD format)
        dropoff_date: Drop-off date (YYYY-MM-DD format)
        pickup_time: Pickup time (HH:MM format, default: 10:00)
        dropoff_time: Drop-off time (HH:MM format, default: 10:00)
        car_type: Type of car (economy, compact, midsize, full-size, luxury, SUV)
        age: Driver age (affects pricing and availability)

    Returns:
        Dict[str, Any]: Search results with car rental options
    """
    try:
        configuration = Configuration.from_runnable_config(config)
        
        # Build search query for car rentals
        search_query = f"car rental {location} {pickup_date} to {dropoff_date}"
        search_query += f" {car_type} car best deals budget hertz avis enterprise"
        if age < 25:
            search_query += " young driver under 25"
        
        # Use Tavily for real car rental search
        wrapped = TavilySearchResults(max_results=configuration.max_search_results)
        search_results = await wrapped.ainvoke({"query": search_query})
        
        # Calculate rental duration
        pickup = datetime.strptime(pickup_date, "%Y-%m-%d")
        dropoff = datetime.strptime(dropoff_date, "%Y-%m-%d")
        rental_days = (dropoff - pickup).days
        
        return {
            "status": "success",
            "search_query": search_query,
            "location": location,
            "pickup_date": pickup_date,
            "dropoff_date": dropoff_date,
            "pickup_time": pickup_time,
            "dropoff_time": dropoff_time,
            "rental_days": rental_days,
            "car_type": car_type,
            "driver_age": age,
            "results": search_results,
            "message": f"Found {car_type} car rental options in {location} for {rental_days} day{'s' if rental_days != 1 else ''}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Car rental search failed: {str(e)}",
            "location": location
        }


def book_car(
    car_id: str,
    driver_name: str,
    email: str,
    phone: str,
    license_number: str,
    pickup_location: str = "Main Terminal"
) -> Dict[str, Any]:
    """Book a car rental (dummy function for demonstration).

    Args:
        car_id: The car rental identifier to book
        driver_name: Name of the primary driver
        email: Contact email
        phone: Contact phone number
        license_number: Driver's license number
        pickup_location: Specific pickup location

    Returns:
        Dict[str, Any]: Booking confirmation details
    """
    # Generate dummy booking confirmation
    confirmation_number = f"CR{random.randint(100000, 999999)}"
    booking_reference = f"TM{random.randint(10000, 99999)}"
    
    return {
        "status": "success",
        "booking_confirmed": True,
        "confirmation_number": confirmation_number,
        "booking_reference": booking_reference,
        "car_id": car_id,
        "driver_name": driver_name,
        "email": email,
        "phone": phone,
        "license_number": license_number,
        "pickup_location": pickup_location,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": f"Car rental booking confirmed! Confirmation number: {confirmation_number}. You will receive an email confirmation at {email}."
    }


def cancel_car(
    confirmation_number: str,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Cancel a car rental booking (dummy function for demonstration).

    Args:
        confirmation_number: The booking confirmation number
        reason: Optional cancellation reason

    Returns:
        Dict[str, Any]: Cancellation confirmation details
    """
    cancellation_id = f"CX{random.randint(100000, 999999)}"
    
    # Random cancellation fee based on timing
    cancellation_fee = random.randint(0, 75)
    
    return {
        "status": "success",
        "cancellation_confirmed": True,
        "cancellation_id": cancellation_id,
        "confirmation_number": confirmation_number,
        "reason": reason,
        "cancellation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "refund_status": "pending",
        "refund_timeline": "5-7 business days",
        "cancellation_fee": cancellation_fee,
        "message": f"Car rental booking {confirmation_number} has been cancelled. Cancellation ID: {cancellation_id}. Refund will be processed within 5-7 business days."
    }


def change_car(
    confirmation_number: str,
    new_pickup_date: Optional[str] = None,
    new_dropoff_date: Optional[str] = None,
    new_pickup_time: Optional[str] = None,
    new_dropoff_time: Optional[str] = None,
    new_car_type: Optional[str] = None,
    new_pickup_location: Optional[str] = None
) -> Dict[str, Any]:
    """Change a car rental booking (dummy function for demonstration).

    Args:
        confirmation_number: The booking confirmation number
        new_pickup_date: New pickup date (YYYY-MM-DD format)
        new_dropoff_date: New drop-off date (YYYY-MM-DD format)
        new_pickup_time: New pickup time (HH:MM format)
        new_dropoff_time: New drop-off time (HH:MM format)
        new_car_type: New car type
        new_pickup_location: New pickup location

    Returns:
        Dict[str, Any]: Change confirmation details
    """
    change_id = f"CH{random.randint(100000, 999999)}"
    change_fee = random.randint(0, 100)
    
    changes_made = []
    if new_pickup_date:
        changes_made.append(f"Pickup date changed to {new_pickup_date}")
    if new_dropoff_date:
        changes_made.append(f"Drop-off date changed to {new_dropoff_date}")
    if new_pickup_time:
        changes_made.append(f"Pickup time changed to {new_pickup_time}")
    if new_dropoff_time:
        changes_made.append(f"Drop-off time changed to {new_dropoff_time}")
    if new_car_type:
        changes_made.append(f"Car type changed to {new_car_type}")
    if new_pickup_location:
        changes_made.append(f"Pickup location changed to {new_pickup_location}")
    
    return {
        "status": "success",
        "change_confirmed": True,
        "change_id": change_id,
        "confirmation_number": confirmation_number,
        "changes_made": changes_made,
        "change_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "change_fee": change_fee,
        "new_pickup_date": new_pickup_date,
        "new_dropoff_date": new_dropoff_date,
        "new_pickup_time": new_pickup_time,
        "new_dropoff_time": new_dropoff_time,
        "new_car_type": new_car_type,
        "new_pickup_location": new_pickup_location,
        "message": f"Car rental booking {confirmation_number} has been changed. Change ID: {change_id}. Change fee: ${change_fee}."
    }


CAR_RENTAL_ASSISTANT_TOOLS: List[Callable[..., Any]] = [
    search_cars,
    book_car,
    cancel_car,
    change_car
] 