"""Define a custom Accommodation Assistant agent.

Works with a chat model with tool calling support.
"""

from typing import Dict, List, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from travel_master.configuration import Configuration
from travel_master.accommodation_assistant.accommodation_assistant_tools import ACCOMMODATION_ASSISTANT_TOOLS
from travel_master.state import InputState, State
from travel_master.utils import load_chat_model


async def accommodation_assistant(
    state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our accommodation assistant.

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)

    # Initialize the model with tool binding
    model = load_chat_model(configuration.sub_assistant_model).bind_tools(ACCOMMODATION_ASSISTANT_TOOLS)

    # Format the system prompt
    system_message = configuration.accommodation_assistant_system_prompt.format(
        system_time=configuration.get_current_time()
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


# Define the accommodation assistant graph
builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the nodes
builder.add_node(accommodation_assistant)
builder.add_node("tools", ToolNode(ACCOMMODATION_ASSISTANT_TOOLS))

# Set the entrypoint
builder.add_edge("__start__", "accommodation_assistant")

# Add conditional edges
builder.add_conditional_edges(
    "accommodation_assistant",
    tools_condition,
)

# Add edge from tools back to accommodation_assistant
builder.add_edge("tools", "accommodation_assistant")

# Compile the graph with recursion limit
graph = builder.compile(
    interrupt_before=[],
    interrupt_after=[],
)
# Set recursion limit
graph = graph.with_config({"recursion_limit": 10})
graph.name = "accommodation_assistant" 