"""Define the Plus Assistant that supervises EAM and Search assistants.

This module creates a supervisor that coordinates between the EAM assistant
and Search assistant to provide comprehensive assistance.
"""

from datetime import datetime
from langgraph_supervisor import create_supervisor

from plus_assistant.eam_assistant.eam_assistant import graph as eam_assistant
from plus_assistant.finance_assistant.finance_assistant import (
    graph as finance_assistant,
)
from plus_assistant.search_assistant.search_assistant import graph as search_assistant
from plus_assistant.utils import load_chat_model
from plus_assistant.configuration import Configuration

# Initialize the model using Configuration
config = Configuration()
model = load_chat_model(config.supervisor_model)

# Get current system time with configured timezone
system_time = config.get_current_time()

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
        "IMPORTANT: When responding to the user:\n"
        "1. Forward the entire message from the sub-assistant without modification if it has follow-up questions. Do not analyze, hallucinate, or take any other actions apart from forwarding the message and assigning tasks to the sub-assistant."
        "2. Include ALL information and details provided by the assistants in your response."
        "3. Present the information as if it's coming directly from you - do not mention which assistant provided what."
        "4. NEVER assume the user has seen any previous information - always provide COMPLETE context."
        "5. Organize the information in a clear, logical flow without revealing the underlying assistant structure."
        "6. Make sure NO important details from any assistant are lost or summarized away."
        "7. Do not summarize or selectively choose which fields to include - you MUST include ALL fields from ALL responses."
        "8. COPY ALL DETAILS EXACTLY as provided by the assistants - do not paraphrase or omit any information."
        f"\n\nSystem time: {system_time} ({config.timezone})"
    )
)

# Compile the workflow and set the name
graph = workflow.compile()
graph.name = "plus_assistant" 
