from enum import EnumType

from pydantic import BaseModel
from typing import get_args, get_origin, List, Dict, Union, Type

from pydantic.fields import FieldInfo


def generate_placeholder(type_: type) -> str:
    origin = get_origin(type_) or type_

    if origin is Union:
        # Handle Optional[X] (which is Union[X, NoneType])
        args = [arg for arg in get_args(type_) if arg is not type(None)]
        return generate_placeholder(args[0]) if args else None

    if issubclass(origin, BaseModel):
        return generate_example_json(origin)

    if origin is list or origin is List:
        placeholder = generate_placeholder(get_args(type_)[0])
        return "[" + placeholder + ", ... ]"

    if origin is dict or origin is Dict:
        key_type, val_type = get_args(type_)
        return "{" + generate_placeholder(key_type) + ':' + generate_placeholder(val_type) + '}'

    # Primitive types
    if origin is str:
        return '"foo" /* or bar, baz, etc. */'
    if origin is int:
        return "0"
    if origin is float:
        return "0.0"
    if origin is bool:
        return "true /* or false */"
    if isinstance(origin, EnumType):
        values = [value.value for value in origin]
        return f'"{values[0]}" /* one of [{values}] */'

    raise TypeError("Unknown type '%s'" % origin)


def generate_example_json(model_cls: type[BaseModel]) -> str:
    return ("{" +
            ",".join([to_example(field_name, model_field) for field_name, model_field in model_cls.model_fields.items()])
            + "}")


def to_example(field_name, model_field: FieldInfo) -> str:
    return (f'"{field_name}":{generate_placeholder(model_field.annotation)} '
            f'/* {model_field.description} {"(required)" if model_field.is_required() else ""} */')
