"""Define an Accommodation Assistant agent."""

from typing import Dict, List, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from plus_assistant.accommodation_assistant.accommodation_assistant_tools import (
    ACCOMMODATION_ASSISTANT_TOOLS,
)
from plus_assistant.configuration import Configuration
from plus_assistant.state import InputState, State
from plus_assistant.utils import load_chat_model


async def accommodation_assistant(
    state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering the accommodation assistant."""
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.sub_assistant_model).bind_tools(
        ACCOMMODATION_ASSISTANT_TOOLS
    )
    system_message = configuration.accommodation_assistant_system_prompt.format(
        system_time=configuration.get_current_time()
    )
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not complete your request.",
                )
            ]
        }
    return {"messages": [response]}


builder = StateGraph(State, input=InputState, config_schema=Configuration)

builder.add_node(accommodation_assistant)
builder.add_node("tools", ToolNode(ACCOMMODATION_ASSISTANT_TOOLS))

builder.add_edge("__start__", "accommodation_assistant")

builder.add_conditional_edges("accommodation_assistant", tools_condition)

builder.add_edge("tools", "accommodation_assistant")

graph = builder.compile(interrupt_before=[], interrupt_after=[])
graph.name = "accommodation_assistant"
