"""Tools for the EAM assistant."""

from typing import Any, Callable, Dict, List, Optional, cast
import json

import aiohttp
from aiohttp import BasicAuth
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from plus_assistant.configuration import Configuration


class WorkRequestClassification(BaseModel):
    """Classification of a work request including type and priority."""

    request_type: str = Field(
        description="The request type code. Must be one of: CLEAN, ELECT, GRAF, PAINT, NA"
    )
    priority: str = Field(
        description="The priority level. Must be one of: HIGH, MED, LOW, NA"
    )


async def create_work_request(
    description: str, details: str, state: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a work request in the EAM system.

    This function uses an internal LLM to classify the request type and priority
    based on the description and details, then creates the work request.

    Args:
        description: Brief description of the work request
        details: Detailed information about the work request
        state: Optional state containing original user input

    Returns:
        Dict[str, Any]: Response containing status and message
    """
    try:
        # Get original user input from state if available
        original_input = (
            state.get("messages", [{}])[-1].get("content", "") if state else ""
        )

        # Initialize LLM with structured output
        llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        structured_llm = llm.with_structured_output(WorkRequestClassification)

        # Create the prompt for classification
        prompt = f"""Based on the work request description and details, determine the most appropriate request type and priority level.

Original User Input: {original_input}
Description: {description}
Details: {details}

Available Request Types:
- CLEAN: Cleaning
- ELECT: Electrical Fault
- GRAF: Graffiti
- PAINT: Painting
- NA: Not Applicable

Available Priority Levels:
- HIGH: High
- MED: Medium
- LOW: Low
- NA: Not Applicable

Please analyze the request and select the most appropriate request type and priority level."""

        # Get classification from LLM and ensure it's the correct type
        classification = await structured_llm.ainvoke(prompt)
        if isinstance(classification, dict):
            classification = WorkRequestClassification(**classification)
        elif not isinstance(classification, WorkRequestClassification):
            raise ValueError("Unexpected classification type")

        # Create the work request
        base_url = "https://saas-dev-sql.onespresso.net/T1Default/CiAnywhere/Web/SAAS-DEV-SQL/Intelligence/InternalApi/Service"
        app_name = "WorkRequests"
        service_name = "WorkRequest.WorkRequestService"
        service_method = "Save"

        url = f"{base_url}?appName={app_name}&serviceName={service_name}&serviceMethod={service_method}"
        headers = {
            "x-t1-api-key": "12f56759-de9c-4f21-a387-8ba48ec1d149",
            "Content-Type": "application/json",
        }
        auth = BasicAuth("HeC", "Keep@training1")

        body = {
            "Items": [
                {
                    "WorkRequestSystemName": "CZZREQASST",
                    "Description": description,
                    "Details": details,
                    "RequestTypeCode": classification.request_type,
                    "PriorityCode": classification.priority,
                    "RequestedBy": "HEC",
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, auth=auth, json=body
            ) as response:
                api_response = await response.text()
                
                # Parse the API response to check for errors
                try:
                    response_json = json.loads(api_response)
                    items = response_json.get("Items", [])
                    if items and items[0].get("Messages"):
                        # If there are messages, check if any are errors
                        error_messages = [
                            msg["Message"] 
                            for msg in items[0]["Messages"] 
                            if msg.get("NotificationType") == "Error"
                        ]
                        if error_messages:
                            return {
                                "status": "error",
                                "message": "Work request creation failed: " + "; ".join(error_messages),
                                "request_type": classification.request_type,
                                "priority": classification.priority,
                                "api_response": api_response
                            }
                    
                    # If we get here and have a work request number, it's a success
                    if items and items[0].get("WorkRequestNumber"):
                        return {
                            "status": "success",
                            "message": f"Work request created successfully with number {items[0]['WorkRequestNumber']}",
                            "request_type": classification.request_type,
                            "priority": classification.priority,
                            "api_response": api_response
                        }
                    
                    # If we get here, something unexpected happened
                    return {
                        "status": "error",
                        "message": "Work request creation failed: Unexpected response format",
                        "request_type": classification.request_type,
                        "priority": classification.priority,
                        "api_response": api_response
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "error",
                        "message": "Work request creation failed: Invalid API response format",
                        "request_type": classification.request_type,
                        "priority": classification.priority,
                        "api_response": api_response
                    }

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}


async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_runnable_config(config)
    wrapped = TavilySearchResults(max_results=configuration.max_search_results)
    result = await wrapped.ainvoke({"query": query})
    return cast(list[dict[str, Any]], result)


EAM_ASSISTANT_TOOLS: List[Callable[..., Any]] = [create_work_request]
