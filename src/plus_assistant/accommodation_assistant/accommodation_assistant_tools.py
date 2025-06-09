"""Tools for the Accommodation Assistant."""

from typing import Any, Callable, List


async def book_accommodation(location: str, nights: int) -> str:
    """Mock booking accommodation."""
    return f"Booked accommodation in {location} for {nights} nights."


async def change_accommodation(booking_id: str, nights: int) -> str:
    """Mock changing accommodation."""
    return f"Changed accommodation {booking_id} to {nights} nights."


async def cancel_accommodation(booking_id: str) -> str:
    """Mock canceling accommodation."""
    return f"Canceled accommodation {booking_id}."


ACCOMMODATION_ASSISTANT_TOOLS: List[Callable[..., Any]] = [
    book_accommodation,
    change_accommodation,
    cancel_accommodation,
]
