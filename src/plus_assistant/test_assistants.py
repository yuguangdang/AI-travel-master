"""Test script to verify the functionality of all assistants."""

import asyncio

from langchain_openai import ChatOpenAI

from plus_assistant.eam_assistant.eam_assistant import graph as eam_assistant
from plus_assistant.plus_assistant import create_plus_assistant
from plus_assistant.search_assistant.search_assistant import graph as search_assistant


async def test_eam_assistant():
    """Test the EAM assistant with a work request question."""
    print("\nTesting EAM Assistant...")
    print("-" * 50)
    
    result = await eam_assistant.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": "I need to register a work request for a broken printer."
            }
        ]
    })
    
    print("EAM Assistant Response:")
    for message in result["messages"]:
        print(message)
    print("-" * 50)

async def test_search_assistant():
    """Test the Search assistant with a search query."""
    print("\nTesting Search Assistant...")
    print("-" * 50)
    
    result = await search_assistant.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": "Find me the cia link"
            }
        ]
    })
    
    print("Search Assistant Response:")
    for message in result["messages"]:
        print(message)
    print("-" * 50)

async def test_plus_assistant():
    """Test the Plus assistant with a question that requires both assistants."""
    print("\nTesting Plus Assistant...")
    print("-" * 50)
    
    # Initialize the model
    model = ChatOpenAI(model="gpt-4o-mini")
    
    # Create the plus assistant
    plus_assistant = create_plus_assistant(model)
    print("\nPlus Assistant created successfully")
    print("-" * 50)

    # Debug: Print the messages we're about to send
    messages = [
        {
            "role": "user",
            "content": "I need to register a work request for a broken printer. Also, find me the cia link."
        }
    ]
    print("\nDebug: Messages to be sent to OpenAI:")
    print(messages)
    print("-" * 50)
    
    try:
        # Test with a question that might need both assistants
        result = await plus_assistant.ainvoke({
            "messages": messages
        })
        
        print("Plus Assistant Response:")
        for message in result["messages"]:
            print(message)
        print("-" * 50)
    except Exception as e:
        print("\nError occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response details: {e.response}")
        print("-" * 50)

async def main():
    """Run all tests."""
    print("Starting assistant tests...")
    # await test_eam_assistant()
    # await test_search_assistant()
    await test_plus_assistant()
    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 