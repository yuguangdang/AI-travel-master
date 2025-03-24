import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from plus_assistant.configuration import Configuration
from plus_assistant.eam_assistant.eam_assistant import graph
from plus_assistant.state import InputState, State

async def test_eam_assistant():
    # Create configuration
    config = Configuration(
        model="openai/gpt-4o-mini",  # Note: format should be provider/model-name
        max_search_results=3,
        eam_assistant_system_prompt=(
            "You are an EAM (Enterprise Asset Management) assistant. "
            "Your role is to help users create and manage work requests. "
            "Current system time: {system_time}"
        )
    )
    
    # Create initial state with a test message
    initial_state = State(
        messages=[{
            "role": "user",
            "content": "I need to create a work request for a broken light fixture in Room 101. "
            "The light has been flickering for the past two days and needs immediate attention "
            "as it's causing eye strain for the employees."
        }],
        is_last_step=False
    )
    
    # Run the graph
    result = await graph.ainvoke(
        InputState(state=initial_state),
        config=config.to_runnable_config()
    )
    
    # Print the conversation
    print("\nConversation:")
    for message in result.state.messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")
        print(f"\n{role.upper()}: {content}")

if __name__ == "__main__":
    # Print OpenAI API key for debugging (first few characters)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        print(f"OpenAI API Key found (starts with: {api_key[:8]}...)")
    else:
        print("Warning: OPENAI_API_KEY not found in environment variables")
    
    asyncio.run(test_eam_assistant()) 