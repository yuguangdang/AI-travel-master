"""Define tools for the Search Assistant agent."""

from typing import Any, Callable, List


def get_cia_links(query: str) -> str:
    """Get links to CIA documents."""
    return "https://www.cia.gov/library/readingroom/docs/CIA-RDP87-00783R000400010001-1.pdf"

SEARCH_ASSISTANT_TOOLS: List[Callable[..., Any]] = [get_cia_links]