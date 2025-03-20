"""Define a custom Search Assistant agent.

Works with a chat model with tool calling support.
"""

from datetime import UTC, datetime
from typing import Dict, List, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from plus_assistant.configuration import Configuration
from plus_assistant.search_assistant.search_assistant_tools import (
    SEARCH_ASSISTANT_TOOLS,
)
from plus_assistant.state import InputState, State
from plus_assistant.utils import load_chat_model


async def search_assistant(
    state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our search assistant.

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)

    # Initialize the model with tool binding
    model = load_chat_model(configuration.model).bind_tools(SEARCH_ASSISTANT_TOOLS)

    # Format the system prompt
    system_message = configuration.search_assistant_system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    # Handle the case when it's the last step and the model still wants to use a tool
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}

# Define the search assistant graph
builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the nodes
builder.add_node(search_assistant)
builder.add_node("tools", ToolNode(SEARCH_ASSISTANT_TOOLS))

# Set the entrypoint
builder.add_edge("__start__", "search_assistant")

# Add conditional edges
builder.add_conditional_edges(
    "search_assistant",
    tools_condition,
)

# Add edge from tools back to search_assistant
builder.add_edge("tools", "search_assistant")

# Compile the graph
graph = builder.compile(
    interrupt_before=[],
    interrupt_after=[],
)
graph.name = "search_assistant" 