"""Tools for the Flight Assistant."""

from typing import Any, Callable, List


async def book_flight(origin: str, destination: str, date: str) -> str:
    """Mock booking a flight."""
    return f"Booked flight from {origin} to {destination} on {date}."


async def change_flight(booking_id: str, new_date: str) -> str:
    """Mock changing a flight."""
    return f"Changed flight {booking_id} to {new_date}."


async def cancel_flight(booking_id: str) -> str:
    """Mock canceling a flight."""
    return f"Canceled flight {booking_id}."


FLIGHT_ASSISTANT_TOOLS: List[Callable[..., Any]] = [
    book_flight,
    change_flight,
    cancel_flight,
]
