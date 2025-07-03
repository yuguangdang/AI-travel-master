import pytest
from langsmith import unit

from travel_master.flight_assistant.flight_assistant import graph as flight_assistant
from travel_master.travel_master import graph as travel_master


@pytest.mark.asyncio
@unit
async def test_flight_assistant_search() -> None:
    """Test that the Flight assistant can handle a basic flight search request."""
    res = await flight_assistant.ainvoke(
        {"messages": [("user", "I need to search for flights from New York to London on December 15th")]},
        {"configurable": {"system_prompt": "You are a Flight Assistant. Your role is to help users search, book, cancel, and change flight reservations."}},
    )

    # Check if the response mentions flight search
    response_content = str(res["messages"][-1].content).lower()
    assert any(keyword in response_content for keyword in ["flight", "search", "new york", "london"])


@pytest.mark.asyncio  
@unit
async def test_travel_master_coordination() -> None:
    """Test that the Travel Master can coordinate travel planning requests."""
    res = await travel_master.ainvoke(
        {"messages": [("user", "I need to plan a trip to Paris: flights, hotel, and car rental")]},
        {"configurable": {"system_prompt": "You are the Travel Master, coordinating between flight, accommodation, and car rental assistants."}},
    )

    # Check if the response mentions travel planning coordination
    response_content = str(res["messages"][-1].content).lower()
    assert any(keyword in response_content for keyword in ["travel", "flight", "hotel", "car rental", "paris"])
