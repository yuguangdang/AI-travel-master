"""Define tools for the Finance Assistant agent."""

from typing import Any, Callable, List


def get_invoice(invoice_id: str) -> str:
    """Get invoice details."""
    return "Invoice #12345 - Amount: $1,000 - Date: 2024-03-20 - Status: Paid"

FINANCE_ASSISTANT_TOOLS: List[Callable[..., Any]] = [get_invoice] 