"""Define the Plus Assistant that supervises EAM and Search assistants.

This module creates a supervisor that coordinates between the EAM assistant
and Search assistant to provide comprehensive assistance.
"""

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor

from plus_assistant.eam_assistant.eam_assistant import graph as eam_assistant
from plus_assistant.finance_assistant.finance_assistant import graph as finance_assistant
from plus_assistant.search_assistant.search_assistant import graph as search_assistant

# Initialize the model
model = ChatOpenAI(model="gpt-4o-mini")

# Create supervisor workflow
workflow = create_supervisor(
    [eam_assistant, search_assistant, finance_assistant],
    model=model,
    prompt=(
        "You are a team supervisor managing an EAM assistant, a search assistant and a finance assistant. "
        "You can use all the assistants to answer the user's question. "
        "Choose the appropriate assistant based on the user's needs."
        "EAM assistant can help create work requests."
        "Search assistant can help find destination url in CiA system."
        "Finance assistant can help get invoice details."
    )
)

# Compile the workflow and set the name
graph = workflow.compile()
graph.name = "plus_assistant" 
