from pytest import raises

from typedpy import schema_definitions_to_code, schema_to_struct_code, write_code_from_schema
from typedpy.structures import *
from typedpy.fields import *

definitions = {
    "SimpleStruct": {
        "type": "object",
        "name": {
            "type": "string",
            "pattern": "[A-Za-z]+$",
            "maxLength": 8
        },
        "required": [
            "name"
        ],
        "additionalProperties": True
    }
}

schema = {
    "type": "object",
    "description": "This is a test of schema mapping",
    "foo": {
        "type": "object",
        "a2": {
            "type": "float"
        },
        "a1": {
            "type": "integer"
        },
        "required": [
            "a2",
            "a1"
        ],
        "additionalProperties": True
    },
    "ss": {
        "$ref": "#/definitions/SimpleStruct"
    },
    "enum": {
        "type": "enum",
        "values": [
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
                "multiplesOf": 5
            },
            {
                "type": "number"
            }
        ]
    },
    "required": [
        "foo",
        "ss",
        "enum",
        "s",
        "i",
        "all",
        "a"
    ],
    "additionalProperties": True,
    "definitions": {
        "SimpleStruct": {
            "type": "object",
            "name": {
                "maxLength": 8,
                "type": "string",
                "pattern": "[A-Za-z]+$"
            },
            "required": [
                "name"
            ],
            "additionalProperties": True
        }
    }
}
def test_definitions():
    code = schema_definitions_to_code(definitions)
    exec(code, globals())
    assert SimpleStruct(name = 'abc').name =='abc'

def test_schema():
    definitions_code = schema_definitions_to_code(definitions)
    exec(definitions_code, globals())

    struct_code = schema_to_struct_code('Duba', schema, definitions)
    exec(struct_code, globals())
    duba = Duba(
        foo = {'a1': 5, 'a2': 1.5},
        ss = SimpleStruct(name = 'abc'),
        enum = 2,
        s = "xyz",
        i = 10,
        all = 6,
        a = [10, 3]
    )
    assert duba.ss.name == 'abc'

def test_write_code_to_file():
    write_code_from_schema(schema, definitions, "generated_sample.py", "Poo")
    from generated_sample import Poo, SimpleStruct
    poo = Poo(
        foo={'a1': 5, 'a2': 1.5},
        ss=SimpleStruct(name='abc'),
        enum=2,
        s="xyz",
        i=10,
        all=6,
        a=[10, 3]
    )
    assert poo.ss.name == 'abc'
    assert 'This is a test of schema mapping'==Poo.__doc__.strip()
    from os import remove
    remove("generated_sample.py")