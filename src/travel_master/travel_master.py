"""Define the Travel Master that supervises Flight, Accommodation, and Car Rental assistants.

This module creates a supervisor that coordinates between the Flight assistant,
Accommodation assistant, and Car Rental assistant to provide comprehensive travel services.
"""

from langgraph_supervisor import create_supervisor

from travel_master.configuration import Configuration
from travel_master.flight_assistant.flight_assistant import graph as flight_assistant
from travel_master.accommodation_assistant.accommodation_assistant import (
    graph as accommodation_assistant,
)
from travel_master.car_rental_assistant.car_rental_assistant import graph as car_rental_assistant
from travel_master.utils import load_chat_model

# Initialize the model using Configuration
config = Configuration()
model = load_chat_model(config.supervisor_model)

# Get current system time with configured timezone
system_time = config.get_current_time()

# Create supervisor workflow with recursion limit
workflow = create_supervisor(
    [flight_assistant, accommodation_assistant, car_rental_assistant],
    model=model,
    prompt=(
        "You are the Travel Master, a team supervisor managing a flight assistant, an accommodation assistant, and a car rental assistant. "
        "You can use all the assistants to help users plan and book their travel needs. "
        "Choose the appropriate assistant based on the user's travel requirements:\n"
        "• Flight assistant can help search, book, cancel, and change flight reservations.\n"
        "• Accommodation assistant can help search, book, cancel, and change hotel and lodging reservations.\n"
        "• Car rental assistant can help search, book, cancel, and change car rental reservations.\n\n"
        "IMPORTANT: When responding to the user:\n"
        "1. Forward the entire message from the sub-assistant without modification if it has follow-up questions. Do not analyze, hallucinate, or take any other actions apart from forwarding the message and assigning tasks to the sub-assistant.\n"
        "2. Include ALL information and details provided by the assistants in your response.\n"
        "3. Present the information as if it's coming directly from you - do not mention which assistant provided what.\n"
        "4. NEVER assume the user has seen any previous information - always provide COMPLETE context.\n"
        "5. Organize the information in a clear, logical flow without revealing the underlying assistant structure.\n"
        "6. Make sure NO important details from any assistant are lost or summarized away.\n"
        "7. Do not summarize or selectively choose which fields to include - you MUST include ALL fields from ALL responses.\n"
        "8. COPY ALL DETAILS EXACTLY as provided by the assistants - do not paraphrase or omit any information.\n"
        "9. When an assistant provides a complete answer, respond to the user immediately without further delegation.\n"
        "10. Only delegate to assistants when the user explicitly asks for travel-related help.\n"
        f"\n\nSystem time: {system_time} ({config.timezone})"
    )
)

# Compile the workflow with recursion limit and set the name
graph = workflow.compile()
# Set recursion limit
graph = graph.with_config({"recursion_limit": 15})
graph.name = "travel_master" 