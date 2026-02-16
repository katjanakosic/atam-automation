import re
from dataclasses import dataclass
from textwrap import dedent
from typing import Type, Callable, Any

import ollama
from langchain_core.messages import ai
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.utils.pydantic import TBaseModel
from langchain_ollama import ChatOllama
from pydantic import TypeAdapter
import requests


from common.llm.json_example import generate_placeholder
from common.llm_access import Prompt, TypedLlm, AiMessage, ResponseType


class OllamaPrompt(Prompt):
    _template: str
    _data: dict[str, Any]
    _formatters: dict[str, Callable[[any], str]] = {}

    def __init__(self, template: str, **kwargs: any):
        self._template = dedent(template)
        self._data = kwargs

    def __setitem__(self, key, value):
        if key == "instruction":
            self._instruction = value
        else:
            self._data[key] = value

    def formatter(self, key: str, fn: Callable[[any], str]):
        self._formatters[key] = fn

    def _format_data(self):
        result = {}
        for key, value in self._data.items():
            if key in self._formatters:
                rendered = self._formatters[key](value)
            else:
                rendered = value

            # escape braces so JSON/examples do not break str.format()
            if isinstance(rendered, str):
                rendered = rendered.replace("{", "{{").replace("}", "}}")

            result[key] = rendered

        return result

    def __str__(self) -> str:
        text = self._template
        for key, value in self._format_data().items():
            text = text.replace("{" + key + "}", str(value))
        return text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}\n{self._template}\n{self._format_data()}"

def _strip_code_fences(text: str) -> str:
    # remove ```json ... ``` or ``` ... ``` if model still produces fenced output

    t = text.strip()

    if t.startswith("```json"):
        t = t[len("```json"):].strip()
        if t.endswith("```"):
            t = t[:-3].strip()
        return t

    if t.startswith("```"):
        t = t[3:].strip()
        if t.endswith("```"):
            t = t[:-3].strip()
        return t

    return t

class OllamaLlmAccess(TypedLlm):
    def __init__(self, model: str, host: str = None):
        self.model = ChatOllama(
            model=model,
            temperature=0.4,
            base_url=host,
            extract_reasoning=True,
        )

    def generate(self, return_type: Type[TBaseModel], prompt: Prompt, debug: Callable[[any], str] = lambda x: x,
                 use_example_for_formatting: bool = True):
        parser = JsonOutputParser(pydantic_object=return_type)

        if use_example_for_formatting:
            prompt["format_instructions"] = (
                    "Return ONLY valid JSON (no markdown, no commentary, no preamble) "
                    "in the same schema as the following example:\n"
                    + generate_placeholder(return_type))
        else:
            prompt["format_instructions"] = parser.get_format_instructions()

        debug(prompt)
        response = self.model.invoke(prompt.__str__())
        debug(response)

        def transform(message: str):
            message = _strip_code_fences(message)
            debug(message)
            return TypeAdapter(return_type).validate_json(message)

        return OllamaAiMessage(response, transform)

    def create_model(self, model_name: str, base_model: str, system_prompt: str):
        self.model._client.create(model=model_name, from_=base_model, system=system_prompt)

    def use_ollama_python(self):
        self.model._client = ollama._client


class OpenRouterLlmAccess(TypedLlm):
    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        temperature: float = 0.4,
        timeout_s: int = 120,
        app_name: str = "atam-automation",
    ):
        self.model_name = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.timeout_s = timeout_s
        self.app_name = app_name

    def generate(self, return_type: Type[TBaseModel], prompt: Prompt, debug: Callable[[any], str] = lambda x: x,
                 use_example_for_formatting: bool = True):
        parser = JsonOutputParser(pydantic_object=return_type)

        if use_example_for_formatting:
            prompt["format_instructions"] = (
                "Return ONLY valid JSON (no markdown, no commentary, no preamble) "
                "in the same schema as the following example:\n"
                + generate_placeholder(return_type)
            )
        else:
            prompt["format_instructions"] = parser.get_format_instructions()

        debug(prompt)

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Title": self.app_name,
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt.__str__()}],
            "temperature": self.temperature,
        }

        r = requests.post(url, headers=headers, json=payload, timeout=self.timeout_s)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]

        def transform(message: str):
            message = _strip_code_fences(message)
            debug(message)
            return TypeAdapter(return_type).validate_json(message)

        msg = type("SimpleMsg", (), {})()
        msg.tool_calls = []
        msg.invalid_tool_calls = []
        msg.usage_metadata = None
        msg.content = content

        return OllamaAiMessage(msg, transform)

@dataclass()
class OllamaAiMessage(AiMessage[ResponseType]):
    def __init__(self, base: ai.BaseMessage, transformer: Callable[[str], ResponseType]):
        self.tool_calls = base.tool_calls
        self.invalid_tool_calls = base.invalid_tool_calls
        self.usage_metadata = base.usage_metadata
        self.original_response = base.content
        self.response = transformer(self.original_response)

