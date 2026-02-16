import os
from typing import Callable, Type, Optional, TypeVar

from langchain_core.messages import ToolCall, InvalidToolCall
from langchain_core.messages.ai import UsageMetadata
from langchain_core.utils.pydantic import TBaseModel

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

class Prompt:
    def formatter(self, key: str, fn: Callable[[any], str]):
        pass

    def __setitem__(self, key, value):
        pass


class TypedLlm:
    def generate(self, return_type: Type[TBaseModel], prompt: Prompt, debug: Callable[[str], str] = lambda x: x,
                 use_example_for_formatting: bool = True):
        pass

    def create_model(self, model_name: str, base_model: str, system_prompt: str):
        pass

    def use_ollama_python(self):
        pass


ResponseType = TypeVar('ResponseType')


class AiMessage[ResponseType]:
    tool_calls: list[ToolCall] = []
    """If provided, tool calls associated with the message."""
    invalid_tool_calls: list[InvalidToolCall] = []
    """If provided, tool calls with parsing errors associated with the message."""
    usage_metadata: Optional[UsageMetadata] = None
    """If provided, usage metadata for a message, such as token counts.

    This is a standard representation of token usage that is consistent across models.
    """


def create_prompt(template: str = None, file: str = None, **kwargs: any) -> Prompt:
    from common.llm.typedllm import OllamaPrompt
    if file is None and template is None:
        raise "You must specify a template or a file"
    elif file is not None and template is not None:
        raise "You cannot specify both a template and a file"
    elif template is not None:
        return OllamaPrompt(template, **kwargs)
    else:
        with open(file, "r") as f:
            return OllamaPrompt(f.read(), **kwargs)



def create_typed_llm(
    model: str,
    host: str = None,
    provider: str = "ollama",
    openrouter_api_key: Optional[str] = None,
    openrouter_base_url: str = "https://openrouter.ai/api/v1",
) -> TypedLlm:
    """
    Create and configure a TypedLlm instance for the selected provider.

    :param model: Model identifier for the selected provider
    :param host: Base URL of the Ollama server
    :param provider: LLM provider (either "ollama" or "openrouter")
    :param openrouter_api_key: OpenRouter API key (if None: value is read from environment variables)
    :param openrouter_base_url: OpenRouter base URL (if None: value is read from environment variables)
    :return: Provider-specific implementation of TypedLlm configured with selected parameters
    """
    provider = os.getenv("ATAM_LLM_PROVIDER", provider)
    model = os.getenv("ATAM_LLM_MODEL", model)
    openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", openrouter_base_url)

    if provider == "openrouter":
        if not openrouter_api_key:
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        if not openrouter_api_key:
            raise ValueError(
                "openrouter_api_key is required when provider='openrouter'. "
                "Set OPENROUTER_API_KEY in env/.env or pass openrouter_api_key=..."
            )
        from common.llm.typedllm import OpenRouterLlmAccess
        return OpenRouterLlmAccess(
            model=model,
            api_key=openrouter_api_key,
            base_url=openrouter_base_url,
            temperature=0.4,
        )

    # default: ollama
    from common.llm.typedllm import OllamaLlmAccess
    return OllamaLlmAccess(model, host=host)
