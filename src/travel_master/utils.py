"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    
    if provider == "azure_openai":
        # For Azure OpenAI, we need to pass additional parameters
        from langchain_openai import AzureChatOpenAI

        from travel_master.configuration import Configuration
        
        # Get configuration
        config = Configuration()
        
        return AzureChatOpenAI(
            model=model,
            api_version=config.azure_api_version,
            azure_endpoint=config.azure_endpoint,
            temperature=0.1
        )
    else:
        return init_chat_model(model, model_provider=provider, temperature=0.1)
