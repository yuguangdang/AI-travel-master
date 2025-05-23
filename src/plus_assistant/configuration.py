"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Annotated, Optional

from langchain_core.runnables import RunnableConfig, ensure_config

from plus_assistant import prompts


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    eam_assistant_system_prompt: str = field(
        default=prompts.EAM_ASSISTANT_SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    search_assistant_system_prompt: str = field(
        default=prompts.SEARCH_ASSISTANT_SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    finance_assistant_system_prompt: str = field(
        default=prompts.FINANCE_ASSISTANT_SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )
    supervisor_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="azure_openai/gpt-4.1",
        metadata={
            "description": "The name of the language model to use for the supervisor's interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    sub_assistant_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="azure_openai/gpt-4.1-mini",
        metadata={
            "description": "The name of the language model to use for the sub-assistants' interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    timezone: str = field(
        default="Australia/Brisbane",
        metadata={
            "description": "The timezone to use for displaying times in system prompts. "
            "Should be a valid IANA timezone string (e.g., 'Australia/Brisbane', 'America/New_York', 'UTC')."
        },
    )

    azure_api_version: str = field(
        default="2025-01-01-preview",
        metadata={
            "description": "The API version to use for Azure OpenAI API calls."
        },
    )

    azure_endpoint: str = field(
        default="https://rony-m6e499ib-eastus2.cognitiveservices.azure.com/",
        metadata={
            "description": "The Azure OpenAI endpoint URL."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})

    def get_current_time(self) -> str:
        """Get the current time in the configured timezone.
        
        Returns:
            str: Current timestamp in ISO format with timezone information.
        """
        from datetime import datetime

        import pytz
        
        tz = pytz.timezone(self.timezone)
        return datetime.now(tz).isoformat()
