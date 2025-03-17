"""Tools for the EAM assistant."""

import aiohttp
from aiohttp import BasicAuth
from typing import Any, Callable, List, Optional, cast
from typing_extensions import Annotated

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg

from react_agent.configuration import Configuration


async def create_work_request(
    description: str,
    details: str
) -> str:
    """Create a work request in the EAM system.

    This function creates a new work request using the Brainy Intelligence API.

    Args:
        description: Brief description of the work request
        details: Detailed information about the work request

    Returns:
        str: Response from the API indicating success or failure
    """
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
                "RequestTypeCode": "NA",
                "PriorityCode": "NA",
                "RequestedBy": "HEC",
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, auth=auth, json=body) as response:
            return await response.text()


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


TOOLS: List[Callable[..., Any]] = [create_work_request]
