"""Define a custom EAM Assistant agent.

Works with a chat model with tool calling support.
"""

from datetime import UTC, datetime
from typing import Dict, List, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from plus_assistant.configuration import Configuration
from plus_assistant.eam_assistant.eam_assistant_tools import EAM_ASSISTANT_TOOLS
from plus_assistant.state import InputState, State
from plus_assistant.utils import load_chat_model

# Define the function that calls the model


async def eam_assistant(
    state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our eam assistant.

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)

    # Initialize the model with tool binding. Change the model or add more tools here.
    model = load_chat_model(configuration.sub_assistant_model).bind_tools(EAM_ASSISTANT_TOOLS)

    # Format the system prompt. Customize this to change the agent's behavior.
    system_message = configuration.eam_assistant_system_prompt.format(
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


# Define a new graph

builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node(eam_assistant)
builder.add_node("tools", ToolNode(EAM_ASSISTANT_TOOLS))

# Set the entrypoint as `eam_assistant`
# This means that this node is the first one called
builder.add_edge("__start__", "eam_assistant")


# Add a conditional edge to determine the next step after `eam_assistant`
builder.add_conditional_edges(
    "eam_assistant",
    # After eam_assistant finishes running, the next node(s) are scheduled
    # based on the output from route_model_output
    tools_condition,
)

# Add a normal edge from `tools` to `eam_assistant`
# This creates a cycle: after using tools, we always return to the model
builder.add_edge("tools", "eam_assistant")

# Compile the builder into an executable graph
# You can customize this by adding interrupt points for state updates
graph = builder.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[],  # Add node names here to update state after they're called
)
graph.name = "eam_assistant"  # This customizes the name in LangSmith
