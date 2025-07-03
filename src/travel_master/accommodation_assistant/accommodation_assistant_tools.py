"""Tools for the Accommodation assistant."""

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


async def search_hotels(
    location: str,
    check_in_date: str,
    check_out_date: str,
    guests: int = 2,
    rooms: int = 1,
    accommodation_type: str = "hotel",
    *,
    config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, Any]:
    """Search for hotels and accommodations using real web search.

    Args:
        location: City or location to search for accommodations
        check_in_date: Check-in date (YYYY-MM-DD format)
        check_out_date: Check-out date (YYYY-MM-DD format)
        guests: Number of guests (default: 2)
        rooms: Number of rooms needed (default: 1)
        accommodation_type: Type of accommodation (hotel, resort, apartment, etc.)

    Returns:
        Dict[str, Any]: Search results with accommodation options
    """
    try:
        configuration = Configuration.from_runnable_config(config)
        
        # Build search query for accommodations
        search_query = f"{accommodation_type}s in {location} {check_in_date} to {check_out_date}"
        search_query += f" {guests} guest{'s' if guests > 1 else ''} {rooms} room{'s' if rooms > 1 else ''}"
        search_query += " best deals booking reviews rates"
        
        # Use Tavily for real accommodation search
        wrapped = TavilySearchResults(max_results=configuration.max_search_results)
        search_results = await wrapped.ainvoke({"query": search_query})
        
        # Calculate number of nights
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
        nights = (check_out - check_in).days
        
        return {
            "status": "success",
            "search_query": search_query,
            "location": location,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "nights": nights,
            "guests": guests,
            "rooms": rooms,
            "accommodation_type": accommodation_type,
            "results": search_results,
            "message": f"Found {accommodation_type} options in {location} for {nights} night{'s' if nights != 1 else ''} ({guests} guest{'s' if guests > 1 else ''})"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Accommodation search failed: {str(e)}",
            "location": location
        }


def book_hotel(
    hotel_id: str,
    guest_name: str,
    email: str,
    phone: str,
    room_type: str = "Standard Room"
) -> Dict[str, Any]:
    """Book a hotel room (dummy function for demonstration).

    Args:
        hotel_id: The hotel identifier to book
        guest_name: Name of the primary guest
        email: Contact email
        phone: Contact phone number
        room_type: Type of room to book

    Returns:
        Dict[str, Any]: Booking confirmation details
    """
    # Generate dummy booking confirmation
    confirmation_number = f"HT{random.randint(100000, 999999)}"
    booking_reference = f"TM{random.randint(10000, 99999)}"
    
    return {
        "status": "success",
        "booking_confirmed": True,
        "confirmation_number": confirmation_number,
        "booking_reference": booking_reference,
        "hotel_id": hotel_id,
        "guest_name": guest_name,
        "email": email,
        "phone": phone,
        "room_type": room_type,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": f"Hotel booking confirmed! Confirmation number: {confirmation_number}. You will receive an email confirmation at {email}."
    }


def cancel_hotel(
    confirmation_number: str,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Cancel a hotel booking (dummy function for demonstration).

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
        "refund_timeline": "3-5 business days",
        "cancellation_fee": random.randint(0, 100),
        "message": f"Hotel booking {confirmation_number} has been cancelled. Cancellation ID: {cancellation_id}. Refund will be processed within 3-5 business days."
    }


def change_hotel(
    confirmation_number: str,
    new_check_in_date: Optional[str] = None,
    new_check_out_date: Optional[str] = None,
    new_guests: Optional[int] = None,
    new_rooms: Optional[int] = None,
    new_room_type: Optional[str] = None
) -> Dict[str, Any]:
    """Change a hotel booking (dummy function for demonstration).

    Args:
        confirmation_number: The booking confirmation number
        new_check_in_date: New check-in date (YYYY-MM-DD format)
        new_check_out_date: New check-out date (YYYY-MM-DD format)
        new_guests: New number of guests
        new_rooms: New number of rooms
        new_room_type: New room type

    Returns:
        Dict[str, Any]: Change confirmation details
    """
    change_id = f"CH{random.randint(100000, 999999)}"
    change_fee = random.randint(25, 150)
    
    changes_made = []
    if new_check_in_date:
        changes_made.append(f"Check-in date changed to {new_check_in_date}")
    if new_check_out_date:
        changes_made.append(f"Check-out date changed to {new_check_out_date}")
    if new_guests:
        changes_made.append(f"Number of guests changed to {new_guests}")
    if new_rooms:
        changes_made.append(f"Number of rooms changed to {new_rooms}")
    if new_room_type:
        changes_made.append(f"Room type changed to {new_room_type}")
    
    return {
        "status": "success",
        "change_confirmed": True,
        "change_id": change_id,
        "confirmation_number": confirmation_number,
        "changes_made": changes_made,
        "change_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "change_fee": change_fee,
        "new_check_in_date": new_check_in_date,
        "new_check_out_date": new_check_out_date,
        "new_guests": new_guests,
        "new_rooms": new_rooms,
        "new_room_type": new_room_type,
        "message": f"Hotel booking {confirmation_number} has been changed. Change ID: {change_id}. Change fee: ${change_fee}."
    }


ACCOMMODATION_ASSISTANT_TOOLS: List[Callable[..., Any]] = [
    search_hotels,
    book_hotel,
    cancel_hotel,
    change_hotel
] 