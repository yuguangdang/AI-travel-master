"""Define tools for the Search Assistant agent."""

from typing import Any, Callable, List


dummy_result = [
    {
        "text": "I have found some options for you. To which page would you like me to take you?"
    },
    {
        "text": "Function Search Results",
        "buttons": [
            {
                "type": "nls",
                "title": "My Reviews",
                "payload": {
                    "redirectTo": "/T1Default/CiAnywhere/Web/SAAS-DEV-SQL/Reviews/ReviewEnquiry?f=$RVW.RVW.LST",
                    "search": "?Function Name Contains report or Title Contains report"
                }
            },
            {
                "type": "nls",
                "title": "All Submissions",
                "payload": {
                    "redirectTo": "/T1Default/CiAnywhere/Web/SAAS-DEV-SQL/StudentAppInterfaces/SubmissionMyEnquiry?f=$SAI.ALLSUBS.LST",
                    "search": "?Function Name Contains registration or Title Contains registration"
                }
            }
        ]
    }
]

def search_item_in_erp_system(query: str) -> str:
    """Get links to CIA documents."""
    return dummy_result

SEARCH_ASSISTANT_TOOLS: List[Callable[..., Any]] = [search_item_in_erp_system]