import pytest
from langsmith import unit

from plus_assistant.flight_assistant.flight_assistant import graph as flight_assistant


@pytest.mark.asyncio
@unit  # type: ignore[misc]
async def test_flight_assistant_booking() -> None:
    """Test that the flight assistant can handle a basic booking."""
    res = await flight_assistant.ainvoke(
        {"messages": [("user", "Book a flight from NYC to LA tomorrow")]},
        {"configurable": {"system_prompt": "You are a flight assistant."}},
    )

    response_content = str(res["messages"][-1].content).lower()
    assert "flight" in response_content
