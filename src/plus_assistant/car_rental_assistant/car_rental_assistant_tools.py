"""Tools for the Car Rental Assistant."""

from typing import Any, Callable, List


async def book_car(model: str, days: int) -> str:
    """Mock booking a car."""
    return f"Booked {model} for {days} days."


async def change_car(booking_id: str, days: int) -> str:
    """Mock changing a car rental."""
    return f"Changed car rental {booking_id} to {days} days."


async def cancel_car(booking_id: str) -> str:
    """Mock canceling a car rental."""
    return f"Canceled car rental {booking_id}."


CAR_RENTAL_ASSISTANT_TOOLS: List[Callable[..., Any]] = [
    book_car,
    change_car,
    cancel_car,
]
