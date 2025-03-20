"""Define the Plus Assistant that supervises EAM and Search assistants.

This module creates a supervisor that coordinates between the EAM assistant
and Search assistant to provide comprehensive assistance.
"""

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor

from plus_assistant.eam_assistant.eam_assistant import graph as eam_assistant
from plus_assistant.search_assistant.search_assistant import graph as search_assistant

# Initialize the model
model = ChatOpenAI(model="gpt-4o-mini")

# Create supervisor workflow
workflow = create_supervisor(
    [eam_assistant, search_assistant],
    model=model,
    prompt=(
        "You are a team supervisor managing an EAM expert and a search expert. "
        "You can use both agents to answer the user's question. "
        "The EAM expert can help with EAM-related tasks, while the search expert "
        "can help find information from the web. "
        "Choose the appropriate expert based on the user's needs."
    )
)

# Compile the workflow and set the name
graph = workflow.compile()
graph.name = "plus_assistant" 
