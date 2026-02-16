from enum import EnumType

from pydantic import BaseModel
from typing import get_args, get_origin, List, Dict, Union, Literal

from pydantic.fields import FieldInfo

def _is_subclass_safe(t, cls) -> bool:
    """
    Safely check whether `t` is a subclass of `cls`.

    Prevents TypeError when `t` is not a concrete class.
    :param t: Candidate object
    :param cls:  Base class to test against (e.g., pydantic.BaseModel)
    :return: True if `t` is a class and issubclass(t, cls) holds; otherwise False
    """
    return isinstance(t, type) and issubclass(t, cls)

def _is_literal_type(type_) -> bool:
    """
    Safely check whether `type_` is a literal type.
    :param type_: Annotation/type object to inspect
    :return: True if `type_` is (or resolves to) a Literal type; otherwise False
    """
    if get_origin(type_) is Literal:
        return True

    return str(type_) == "typing.Literal" or str(get_origin(type_) or type_) == "typing.Literal"


def generate_placeholder(type_: type) -> str:
    """
    Generate a placeholder/example value (as a string) for the given type annotation.

    Used to create an "example JSON-like schema" that can be embedded into LLM prompts as formatting guidance.
    :param type_: Python type or typing annotation
    :return: A string representing an example value for the given type
    """
    origin = get_origin(type_) or type_

    if origin is Union:
        args = [arg for arg in get_args(type_) if arg is not type(None)]
        return generate_placeholder(args[0]) if args else None

    if _is_literal_type(type_):
        args = get_args(type_)
        if args:
            return f"{args[0]!r}"
        return "null"

    if _is_subclass_safe(origin, BaseModel):
        return generate_example_json(origin)

    if origin is list or origin is List:
        elem_type = get_args(type_)[0] if get_args(type_) else str
        placeholder = generate_placeholder(elem_type)
        return "[" + placeholder + ", ... ]"

    if origin is dict or origin is Dict:
        args = get_args(type_)
        if len(args) == 2:
            key_type, val_type = args
        else:
            key_type, val_type = str, str
        return "{" + generate_placeholder(key_type) + ":" + generate_placeholder(val_type) + "}"

    if origin is str:
        return '"foo"'
    if origin is int:
        return "0"
    if origin is float:
        return "0.0"
    if origin is bool:
        return "true"

    if isinstance(origin, EnumType):
        values = [value.value for value in origin]
        return f'"{values[0]}"' if values else '"UNKNOWN"'

    raise TypeError(f"Unknown type '{origin}'")


def generate_example_json(model_cls: type[BaseModel]) -> str:
    return ("{" +
            ",".join([to_example(field_name, model_field) for field_name, model_field in model_cls.model_fields.items()])
            + "}")


def to_example(field_name, model_field: FieldInfo) -> str:
    """
    Render a single field entry for the example JSON-like model output.

    :param field_name: Name of the field in the Pydantic model
    :param model_field: Pydantic FieldInfo describing the field, including annotation and metadata
    :return: A string representing a JSON-like entry for this field
    """
    placeholder = generate_placeholder(model_field.annotation)
    description = model_field.description or ""
    required = " (required)" if model_field.is_required() else ""

    return f'"{field_name}": {placeholder} /* {description}{required} */'