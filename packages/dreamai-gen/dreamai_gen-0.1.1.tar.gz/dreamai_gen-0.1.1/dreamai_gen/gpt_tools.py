from .utils import *

def get_type_descriptor(t: type) -> dict:
    if t == str:
        return {"type": "string"}
    elif t == int:
        return {"type": "integer"}
    elif t == float or t == int | float:
        return {"type": "number"}
    elif t == bool:
        return {"type": "boolean"}
    elif t == type(None):
        return {"type": "null"}
    elif t == list:
        return {"type": "array"}
    elif t == dict:
        return {"type": "object"}
    elif type(t) == types.GenericAlias:
        if t.__origin__ == list:
            return {"type": "array", "items": get_type_descriptor(t.__args__[0])}
        elif t.__origin__ == dict:
            if t.__args__[0] != str:
                raise ValueError(f"Unsupported type (JSON keys must be strings): { t}")
            return {
                "type": "object",
                "patternProperties": {".*": get_type_descriptor(t.__args__[1])},
            }
        else:
            raise ValueError(f"Unsupported type: {t}")
    elif type(t) == typing._LiteralGenericAlias:
        for arg in t.__args__:
            if type(arg) != type(t.__args__[0]):
                raise ValueError(f"Unsupported type (definite type is required): {t}")
        return {**get_type_descriptor(type(t.__args__[0])), "enum": t.__args__}
    else:
        raise ValueError(f"Unsupported type: {t}")


def generate_function_info(fn):
    docstring = docstring_parser.parse(fn.__doc__)
    short_description = docstring.short_description
    long_description = docstring.long_description
    description = ""
    for desc in [short_description, long_description]:
        if desc:
            description += desc + "\n"
    description = cleandoc(description)

    sig = inspect.signature(fn)
    params = sig.parameters

    function_info = {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    param.arg_name: {
                        "type": get_type_descriptor(eval(param.type_name))["type"],
                        "description": param.description,
                    }
                    for param in docstring.params
                },
                "required": [
                    param.arg_name
                    for param in docstring.params
                    if params[param.arg_name].default is inspect._empty
                ],
            },
        },
    }

    return function_info
