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
                result[key] = self._formatters[key](value)
            else:
                result[key] = value
        return result

    def __str__(self) -> str:
        return self._template.format(**self._format_data())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}\n{self._template}\n{self._format_data()}"


class OllamaLlmAccess(TypedLlm):
    def __init__(self, model: str, host: str = None):
        self.model = ChatOllama(
            model=model,
            temperature=0,
            # format="json",
            base_url=host,
            extract_reasoning=True,
            # other params...
        )

    def generate(self, return_type: Type[TBaseModel], prompt: Prompt, debug: Callable[[any], str] = lambda x: x,
                 use_example_for_formatting: bool = True):
        parser = JsonOutputParser(pydantic_object=return_type)

        if use_example_for_formatting:
            prompt["format_instructions"] = (
                    "Follow a JSON syntax in the same schema as the following example:\n```json\n"
                    + generate_placeholder(return_type) + "\n```\nDo not output anything else.")
        else:
            prompt["format_instructions"] = parser.get_format_instructions()

        debug(prompt)
        response = self.model.invoke(prompt.__str__())
        debug(response)

        def transform(message: str):
            message = message.strip()
            if message.startswith("```json") and message.endswith("```"):
                message = message[len("```json"): -len("```")].strip()

            debug(message)
            return TypeAdapter(return_type).validate_json(message)

        return OllamaAiMessage(response, transform)

        # chain = prompt_text | debug | self.model | debug | TypeAdapter(return_type).validate_json

        # response = chain.invoke({"input": prompt.__str__()})

        # try:
        #    return return_type(**response)
        # except Exception as e:
        #    if retry_count <= 0:
        #        raise Exception(f"Error parsing LLM response.\nWas:\n{response}\nOriginal Error:\n{e}")
        #    else:
        #        return self.generate(return_type, prompt, debug, retry_count - 1)

    def create_model(self, model_name: str, base_model: str, system_prompt: str):
        self.model._client.create(model=model_name, from_=base_model, system=system_prompt)

    def use_ollama_python(self):
        self.model._client = ollama._client


@dataclass()
class OllamaAiMessage(AiMessage[ResponseType]):
    def __init__(self, base: ai.BaseMessage, transformer: Callable[[str], ResponseType]):
        self.tool_calls = base.tool_calls
        self.invalid_tool_calls = base.invalid_tool_calls
        self.usage_metadata = base.usage_metadata
        self.original_response = base.content
        self.response = transformer(self.original_response)

