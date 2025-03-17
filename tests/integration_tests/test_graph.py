import pytest
from langsmith import unit

from react_agent import graph


@pytest.mark.asyncio
@unit
async def test_eam_assistant_work_request() -> None:
    """Test that the EAM assistant can handle a basic work request."""
    res = await graph.ainvoke(
        {"messages": [("user", "I need to create a work request for a broken AC in room 101")]},
        {"configurable": {"system_prompt": "You are an Enterprise Asset Management assistant. Your role is to help users create and manage work requests for facility maintenance and repairs."}},
    )

    # Check if the response mentions creating a work request
    response_content = str(res["messages"][-1].content).lower()
    assert any(keyword in response_content for keyword in ["work request", "maintenance", "repair"])
