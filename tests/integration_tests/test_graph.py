import pytest
from langsmith import unit

from plus_assistant.eam_assistant.eam_assistant import graph as eam_assistant


@pytest.mark.asyncio
@unit
async def test_eam_assistant_work_request() -> None:
    """Test that the EAM assistant can handle a basic work request."""
    res = await eam_assistant.ainvoke(
        {"messages": [("user", "I need to create a work request for a broken AC in room 101")]},
        {"configurable": {"system_prompt": "You are an Enterprise Asset Management assistant. Your role is to help users create and manage work requests for facility maintenance and repairs."}},
    )

    # Check if the response mentions creating a work request
    response_content = str(res["messages"][-1].content).lower()
    assert any(keyword in response_content for keyword in ["work request", "maintenance", "repair"])
