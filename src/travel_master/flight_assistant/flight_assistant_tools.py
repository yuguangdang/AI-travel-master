"""Tools for the Flight assistant."""

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


async def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
    *,
    config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, Any]:
    """Search for flights using real web search.

    Args:
        origin: Departure city or airport code
        destination: Arrival city or airport code  
        departure_date: Departure date (YYYY-MM-DD format)
        return_date: Return date for round trip (YYYY-MM-DD format, optional)
        passengers: Number of passengers (default: 1)

    Returns:
        Dict[str, Any]: Search results with flight options
    """
    try:
        configuration = Configuration.from_runnable_config(config)
        
        # Build search query for flights
        trip_type = "round trip" if return_date else "one way"
        search_query = f"flights from {origin} to {destination} {departure_date}"
        if return_date:
            search_query += f" return {return_date}"
        search_query += f" {passengers} passenger{'s' if passengers > 1 else ''} best deals airlines"
        
        # Use Tavily for real flight search
        wrapped = TavilySearchResults(max_results=configuration.max_search_results)
        search_results = await wrapped.ainvoke({"query": search_query})
        
        return {
            "status": "success",
            "search_query": search_query,
            "trip_type": trip_type,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "passengers": passengers,
            "results": search_results,
            "message": f"Found flight options for {trip_type} from {origin} to {destination}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Flight search failed: {str(e)}",
            "origin": origin,
            "destination": destination
        }


def book_flight(
    flight_id: str,
    passenger_name: str,
    email: str,
    phone: str
) -> Dict[str, Any]:
    """Book a flight (dummy function for demonstration).

    Args:
        flight_id: The flight identifier to book
        passenger_name: Name of the passenger
        email: Contact email
        phone: Contact phone number

    Returns:
        Dict[str, Any]: Booking confirmation details
    """
    # Generate dummy booking confirmation
    confirmation_number = f"FL{random.randint(100000, 999999)}"
    booking_reference = f"TM{random.randint(10000, 99999)}"
    
    return {
        "status": "success",
        "booking_confirmed": True,
        "confirmation_number": confirmation_number,
        "booking_reference": booking_reference,
        "flight_id": flight_id,
        "passenger_name": passenger_name,
        "email": email,
        "phone": phone,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": f"Flight booking confirmed! Confirmation number: {confirmation_number}. You will receive an email confirmation at {email}."
    }


def cancel_flight(
    confirmation_number: str,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Cancel a flight booking (dummy function for demonstration).

    Args:
        confirmation_number: The booking confirmation number
        reason: Optional cancellation reason

    Returns:
        Dict[str, Any]: Cancellation confirmation details
    """
    cancellation_id = f"CX{random.randint(100000, 999999)}"
    
    return {
        "status": "success",
        "cancellation_confirmed": True,
        "cancellation_id": cancellation_id,
        "confirmation_number": confirmation_number,
        "reason": reason,
        "cancellation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "refund_status": "pending",
        "refund_timeline": "5-7 business days",
        "message": f"Flight booking {confirmation_number} has been cancelled. Cancellation ID: {cancellation_id}. Refund will be processed within 5-7 business days."
    }


def change_flight(
    confirmation_number: str,
    new_departure_date: Optional[str] = None,
    new_return_date: Optional[str] = None,
    new_passengers: Optional[int] = None
) -> Dict[str, Any]:
    """Change a flight booking (dummy function for demonstration).

    Args:
        confirmation_number: The booking confirmation number
        new_departure_date: New departure date (YYYY-MM-DD format)
        new_return_date: New return date (YYYY-MM-DD format)
        new_passengers: New number of passengers

    Returns:
        Dict[str, Any]: Change confirmation details
    """
    change_id = f"CH{random.randint(100000, 999999)}"
    change_fee = random.randint(50, 200)
    
    changes_made = []
    if new_departure_date:
        changes_made.append(f"Departure date changed to {new_departure_date}")
    if new_return_date:
        changes_made.append(f"Return date changed to {new_return_date}")
    if new_passengers:
        changes_made.append(f"Number of passengers changed to {new_passengers}")
    
    return {
        "status": "success",
        "change_confirmed": True,
        "change_id": change_id,
        "confirmation_number": confirmation_number,
        "changes_made": changes_made,
        "change_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "change_fee": change_fee,
        "new_departure_date": new_departure_date,
        "new_return_date": new_return_date,
        "new_passengers": new_passengers,
        "message": f"Flight booking {confirmation_number} has been changed. Change ID: {change_id}. Change fee: ${change_fee}."
    }


FLIGHT_ASSISTANT_TOOLS: List[Callable[..., Any]] = [
    search_flights,
    book_flight,
    cancel_flight,
    change_flight
] 