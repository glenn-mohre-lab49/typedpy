from pytest import raises

from typedpy import schema_definitions_to_code, schema_to_struct_code, write_code_from_schema
from typedpy.structures import *
from typedpy.fields import *

components_schemas = {
    "User": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "maxLength": 16,
                "pattern": "[A-Za-z]+$",
                "default": "John"
            },
            "id": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "required": True
            }
        },
        # note that not every additionalProperties option is supported. For example,
        # you can't do "additionalProperties" : { "type": "String" }.
        "additionalProperties": True
    }
}

schema = {
    "type": "object",
    "properties": {
        "foo": {
            "type": "object",
            "properties": {
                "a2": {
                    "type": "float",
                    "required": True
                },
                "a1": {
                    "type": "integer"
                },
            },
            "additionalProperties": True
        },
        "users": {
            "type": "array",
            "items": {
                "$ref": "#/components/schemas/User"
            }
        },
        "en": {
            "type": "integer",
            "enum": [
                1,
                2,
                3
            ]
        },
        "s": {
            "maxLength": 5,
            "type": "string"
        },
        "i": {
            "type": "integer",
            "maximum": 10
        },
        "all": {
            "allOf": [
                {
                    "type": "number"
                },
                {
                    "type": "integer"
                }
            ]
        },
        "a": {
            "type": "array",
            "items": [
                {
                    "type": "integer",
                    "multipleOf": 5
                },
                {
                    "type": "number"
                }
            ]
        }
    },
    "additionalProperties": True,
}


def test_definitions():
    code = schema_definitions_to_code(components_schemas)
    exec(code, globals())
    assert User(id=10, name='Jeff').name == 'Jeff'
