"""Define the Travel Master supervisor.

This module creates a supervisor that coordinates the flight, accommodation and
car rental assistants to provide comprehensive travel planning support.
"""

from langgraph_supervisor import create_supervisor

from plus_assistant.accommodation_assistant.accommodation_assistant import (
    graph as accommodation_assistant,
)
from plus_assistant.car_rental_assistant.car_rental_assistant import (
    graph as car_rental_assistant,
)
from plus_assistant.configuration import Configuration
from plus_assistant.flight_assistant.flight_assistant import graph as flight_assistant
from plus_assistant.utils import load_chat_model

# Initialize the model using Configuration
config = Configuration()
model = load_chat_model(config.supervisor_model)

# Get current system time with configured timezone
system_time = config.get_current_time()

# Create supervisor workflow
workflow = create_supervisor(
    [flight_assistant, accommodation_assistant, car_rental_assistant],
    model=model,
    prompt=(
        "You are a team supervisor managing a flight assistant, an accommodation assistant and a car rental assistant. "
        "You can use all the assistants to answer the user's question. "
        "Choose the appropriate assistant based on the user's needs."
        "Flight assistant can book, change or cancel flights."
        "Accommodation assistant can manage hotel reservations."
        "Car rental assistant can manage vehicle bookings."
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
    ),
)

# Compile the workflow and set the name
graph = workflow.compile()
graph.name = "travel_master"
