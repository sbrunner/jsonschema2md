"""Test jsonschema2md."""

import jsonschema2md


class TestDraft201909defs:
    """Test."""

    test_schema = {
        "$id": "https://example.com/arrays.schema.json",
        "$schema": "http://json-schema.org/draft/2019-09/schema",
        "description": "Food preferences",
        "type": "object",
        "additionalProperties": {
            "description": "Additional info about foods you may like",
            "type": "object",
            "patternProperties": {
                "^iLike(Meat|Drinks)$": {
                    "type": "boolean",
                    "description": "Do I like it?",
                },
            },
        },
        "unevaluatedProperties": {
            "description": "Anything else you want to add",
            "type": "object",
            "additionalProperties": False,
            "patternProperties": {
                "^extraInfo[\\w]*$": {
                    "type": "string",
                    "description": "Anything else I might like to say.",
                },
            },
        },
        "properties": {
            "fruits": {"type": "array", "items": {"type": "string"}},
            "vegetables": {"type": "array", "uniqueItems": True, "items": {"$ref": "#/$defs/veggie"}},
            "taste": {
                "type": "string",
                "description": "How does it taste?",
                "default": "good",
                "pattern": "^[a-z]*$",
            },
        },
        "required": ["fruits"],
        "$defs": {
            "veggie": {
                "type": "object",
                "required": ["veggieName", "veggieLike"],
                "properties": {
                    "veggieName": {
                        "type": "string",
                        "description": "The name of the vegetable.",
                        "minLength": 1,
                        "maxLength": 100,
                    },
                    "veggieLike": {
                        "type": "boolean",
                        "deprecated": False,
                        "description": "Do I like this vegetable?",
                    },
                    "foodLike": {
                        "type": "boolean",
                        "deprecated": True,
                        "description": "Do I like this food?",
                    },
                    "expiresAt": {
                        "type": "string",
                        "format": "date",
                        "description": "When does the veggie expires",
                    },
                },
            },
        },
        "examples": [
            {
                "fruits": ["apple", "orange"],
                "vegetables": [{"veggieName": "cabbage", "veggieLike": True}],
            },
        ],
    }

    def test_parse_schema(self):
        """Test."""
        parser = jsonschema2md.Parser()
        expected_output = [
            "# JSON Schema\n\n",
            "*Food preferences*\n\n",
            "## Additional Properties\n\n",
            '- <a id="additionalProperties"></a>**Additional Properties** *(object)*: '
            "Additional info about foods you may like.\n",
            "  - <a "
            'id="additionalProperties/patternProperties/%5EiLike%28Meat%7CDrinks%29%24"></a>**`^iLike(Meat|Drinks)$`** '
            "*(boolean)*: Do I like it?\n",
            "## Unevaluated Properties\n\n",
            '- <a id="unevaluatedProperties"></a>**Unevaluated Properties** '
            "*(object)*: Anything else you want to add. Cannot contain additional "
            "properties.\n",
            "  - <a "
            'id="unevaluatedProperties/patternProperties/%5EextraInfo%5B%5Cw%5D%2A%24"></a>**`^extraInfo[\\w]*$`** '
            "*(string)*: Anything else I might like to say.\n",
            "## Properties\n\n",
            '- <a id="properties/fruits"></a>**`fruits`** *(array, required)*\n',
            '  - <a id="properties/fruits/items"></a>**Items** *(string)*\n',
            '- <a id="properties/vegetables"></a>**`vegetables`** *(array)*: Items must be unique.\n',
            '  - <a id="properties/vegetables/items"></a>**Items**: Refer to '
            "*[#/$defs/veggie](#%24defs/veggie)*.\n",
            '- <a id="properties/taste"></a>**`taste`** *(string)*: How does it taste? '
            "Must match pattern: `^[a-z]*$` "
            "([Test](https://regexr.com/?expression=%5E%5Ba-z%5D%2A%24)). Default: "
            '`"good"`.\n',
            "## Definitions\n\n",
            '- <a id="%24defs/veggie"></a>**`veggie`** *(object)*\n',
            '  - <a id="%24defs/veggie/properties/veggieName"></a>**`veggieName`** '
            "*(string, required)*: The name of the vegetable. Length must be between 1 "
            "and 100 (inclusive).\n",
            '  - <a id="%24defs/veggie/properties/veggieLike"></a>**`veggieLike`** '
            "*(boolean, required)*: Do I like this vegetable?\n",
            '  - <a id="%24defs/veggie/properties/expiresAt"></a>**`expiresAt`** '
            "*(string, format: date)*: When does the veggie expires.\n",
            "## Examples\n\n",
            "  ```json\n"
            "  {\n"
            '      "fruits": [\n'
            '          "apple",\n'
            '          "orange"\n'
            "      ],\n"
            '      "vegetables": [\n'
            "          {\n"
            '              "veggieName": "cabbage",\n'
            '              "veggieLike": true\n'
            "          }\n"
            "      ]\n"
            "  }\n"
            "  ```\n"
            "\n",
        ]
        assert expected_output == parser.parse_schema(self.test_schema)


class TestParser:
    """Test."""

    test_schema = {
        "$id": "https://example.com/arrays.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "Food preferences",
        "type": "object",
        "additionalProperties": {
            "description": "Additional info about foods you may like",
            "type": "object",
            "patternProperties": {
                "^iLike(Meat|Drinks)$": {
                    "type": "boolean",
                    "description": "Do I like it?",
                },
            },
        },
        "properties": {
            "fruits": {"type": "array", "items": {"type": "string"}},
            "vegetables": {"type": "array", "items": {"$ref": "#/definitions/veggie"}},
            "cakes": {"type": "array", "maxContains": 3, "contains": {"$ref": "#/definitions/cake"}},
        },
        "definitions": {
            "veggie": {
                "type": "object",
                "required": ["veggieName", "veggieLike"],
                "dependentRequired": {"veggieLike": ["expiresAt"]},
                "properties": {
                    "veggieName": {
                        "type": "string",
                        "description": "The name of the vegetable.",
                    },
                    "veggieLike": {
                        "type": "boolean",
                        "description": "Do I like this vegetable?",
                    },
                    "expiresAt": {
                        "type": "string",
                        "format": "date",
                        "description": "When does the veggie expires",
                    },
                },
            },
            "cake": {
                "description": "A cake",
                "type": "string",
            },
        },
        "examples": [
            {
                "fruits": ["apple", "orange"],
                "vegetables": [{"veggieName": "cabbage", "veggieLike": True}],
            },
        ],
    }

    def test_construct_description_line(self):
        """Test."""
        test_cases = [
            {"input": {}, "add_type": False, "expected_output": ""},
            {
                "input": {
                    "description": "The name of the vegetable.",
                },
                "add_type": False,
                "expected_output": ": The name of the vegetable.",
            },
            {
                "input": {
                    "description": "The name of the vegetable.",
                    "default": "eggplant",
                    "type": "string",
                    "$ref": "#/definitions/veggies",
                    "enum": ["eggplant", "spinach", "cabbage"],
                },
                "add_type": True,
                "expected_output": (
                    ": The name of the vegetable. Must be of type *string*. "
                    'Must be one of: `["eggplant", "spinach", "cabbage"]`. '
                    "Refer to *[#/definitions/veggies](#definitions/veggies)*. "
                    'Default: `"eggplant"`.'
                ),
            },
            {
                "input": {
                    "description": "Number of vegetables",
                    "default": 0,
                    "type": "number",
                    "minimum": 0,
                    "maximum": 999,
                    "additionalProperties": True,
                },
                "add_type": False,
                "expected_output": (
                    ": Number of vegetables. Minimum: `0`. Maximum: `999`. "
                    "Can contain additional properties. Default: `0`."
                ),
            },
            {
                "input": {
                    "description": "Number of vegetables",
                    "default": 1,
                    "type": "integer",
                    "exclusiveMinimum": 0,
                    "exclusiveMaximum": 1000,
                },
                "add_type": False,
                "expected_output": (
                    ": Number of vegetables. Exclusive minimum: `0`. Exclusive maximum: `1000`. Default: `1`."
                ),
            },
            {
                "input": {
                    "description": "List of vegetables",
                    "default": [],
                    "type": "array",
                    "additionalProperties": False,
                },
                "add_type": False,
                "expected_output": (
                    ": List of vegetables. Cannot contain additional properties. Default: `[]`."
                ),
            },
            {
                "input": {
                    "description": "List of vegetables",
                    "default": ["Carrot"],
                    "type": "array",
                    "minItems": 1,
                },
                "add_type": False,
                "expected_output": (
                    ': List of vegetables. Length must be at least 1. Default: `["Carrot"]`.'
                ),
            },
            {
                "input": {
                    "description": "List of vegetables",
                    "default": ["Carrot"],
                    "type": "array",
                    "maxItems": 10,
                },
                "add_type": False,
                "expected_output": (
                    ': List of vegetables. Length must be at most 10. Default: `["Carrot"]`.'
                ),
            },
            {
                "input": {
                    "description": "List of vegetables",
                    "default": ["Carrot"],
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 10,
                },
                "add_type": False,
                "expected_output": (
                    ": List of vegetables. "
                    "Length must be between 1 and 10 (inclusive). "
                    'Default: `["Carrot"]`.'
                ),
            },
            {
                "input": {
                    "description": "List of vegetables",
                    "default": ["Carrot", "Mushroom", "Cabbage", "Broccoli", "Leek"],
                    "type": "array",
                    "minItems": 5,
                    "maxItems": 5,
                },
                "add_type": False,
                "expected_output": (
                    ": List of vegetables. "
                    "Length must be equal to 5. "
                    'Default: `["Carrot", "Mushroom", "Cabbage", "Broccoli", "Leek"]`.'
                ),
            },
        ]

        parser = jsonschema2md.Parser()

        for case in test_cases:
            observed_output = " ".join(
                parser._construct_description_line(case["input"], add_type=case["add_type"]),
            )
            assert case["expected_output"] == observed_output

    def test_parse_object(self):
        """Test."""
        parser = jsonschema2md.Parser()
        expected_output = [
            '- <a id="properties/fruits"></a>**`fruits`** *(array)*\n',
            '  - <a id="properties/fruits/items"></a>**Items** *(string)*\n',
        ]
        assert expected_output == parser._parse_object(
            self.test_schema["properties"]["fruits"], "fruits", path=["properties", "fruits"]
        )

    def test_parse_schema(self):
        """Test."""
        parser = jsonschema2md.Parser()
        expected_output = [
            "# JSON Schema\n\n",
            "*Food preferences*\n\n",
            "## Additional Properties\n\n",
            '- <a id="additionalProperties"></a>**Additional Properties** *(object)*: '
            "Additional info about foods you may like.\n",
            "  - <a "
            'id="additionalProperties/patternProperties/%5EiLike%28Meat%7CDrinks%29%24"></a>**`^iLike(Meat|Drinks)$`** '
            "*(boolean)*: Do I like it?\n",
            "## Properties\n\n",
            '- <a id="properties/fruits"></a>**`fruits`** *(array)*\n',
            '  - <a id="properties/fruits/items"></a>**Items** *(string)*\n',
            '- <a id="properties/vegetables"></a>**`vegetables`** *(array)*\n',
            '  - <a id="properties/vegetables/items"></a>**Items**: Refer to '
            "*[#/definitions/veggie](#definitions/veggie)*.\n",
            '- <a id="properties/cakes"></a>**`cakes`** *(array)*: Contains schema '
            "must be matched at most 3 times.\n",
            '  - <a id="properties/cakes/contains"></a>**Contains**: Refer to '
            "*[#/definitions/cake](#definitions/cake)*.\n",
            "## Definitions\n\n",
            '- <a id="definitions/veggie"></a>**`veggie`** *(object)*\n',
            '  - <a id="definitions/veggie/properties/veggieName"></a>**`veggieName`** '
            "*(string, required)*: The name of the vegetable.\n",
            '  - <a id="definitions/veggie/properties/veggieLike"></a>**`veggieLike`** '
            "*(boolean, required)*: Do I like this vegetable?\n",
            '  - <a id="definitions/veggie/properties/expiresAt"></a>**`expiresAt`** '
            "*(string, format: date, required <sub><sup>if `veggieLike` is "
            "set</sup></sub>)*: When does the veggie expires.\n",
            '- <a id="definitions/cake"></a>**`cake`** *(string)*: A cake.\n',
            "## Examples\n\n",
            "  ```json\n"
            "  {\n"
            '      "fruits": [\n'
            '          "apple",\n'
            '          "orange"\n'
            "      ],\n"
            '      "vegetables": [\n'
            "          {\n"
            '              "veggieName": "cabbage",\n'
            '              "veggieLike": true\n'
            "          }\n"
            "      ]\n"
            "  }\n"
            "  ```\n"
            "\n",
        ]
        assert expected_output == parser.parse_schema(self.test_schema)

    def test_parse_schema_examples_yaml(self):
        """Test."""
        parser = jsonschema2md.Parser(examples_as_yaml=True)
        expected_output = [
            "# JSON Schema\n\n",
            "*Food preferences*\n\n",
            "## Additional Properties\n\n",
            '- <a id="additionalProperties"></a>**Additional Properties** *(object)*: '
            "Additional info about foods you may like.\n",
            "  - <a "
            'id="additionalProperties/patternProperties/%5EiLike%28Meat%7CDrinks%29%24"></a>**`^iLike(Meat|Drinks)$`** '
            "*(boolean)*: Do I like it?\n",
            "## Properties\n\n",
            '- <a id="properties/fruits"></a>**`fruits`** *(array)*\n',
            '  - <a id="properties/fruits/items"></a>**Items** *(string)*\n',
            '- <a id="properties/vegetables"></a>**`vegetables`** *(array)*\n',
            '  - <a id="properties/vegetables/items"></a>**Items**: Refer to '
            "*[#/definitions/veggie](#definitions/veggie)*.\n",
            '- <a id="properties/cakes"></a>**`cakes`** *(array)*: Contains schema '
            "must be matched at most 3 times.\n",
            '  - <a id="properties/cakes/contains"></a>**Contains**: Refer to '
            "*[#/definitions/cake](#definitions/cake)*.\n",
            "## Definitions\n\n",
            '- <a id="definitions/veggie"></a>**`veggie`** *(object)*\n',
            '  - <a id="definitions/veggie/properties/veggieName"></a>**`veggieName`** '
            "*(string, required)*: The name of the vegetable.\n",
            '  - <a id="definitions/veggie/properties/veggieLike"></a>**`veggieLike`** '
            "*(boolean, required)*: Do I like this vegetable?\n",
            '  - <a id="definitions/veggie/properties/expiresAt"></a>**`expiresAt`** '
            "*(string, format: date, required <sub><sup>if `veggieLike` is "
            "set</sup></sub>)*: When does the veggie expires.\n",
            '- <a id="definitions/cake"></a>**`cake`** *(string)*: A cake.\n',
            "## Examples\n\n",
            "  ```yaml\n"
            "  fruits:\n"
            "  - apple\n"
            "  - orange\n"
            "  vegetables:\n"
            "  -   veggieName: cabbage\n"
            "      veggieLike: true\n"
            "  ```\n"
            "\n",
        ]
        assert expected_output == parser.parse_schema(self.test_schema)

    def test_parse_top_level_pattern_properties(self):
        """Test."""
        parser = jsonschema2md.Parser()

        test_schema = {
            "$id": "https://example.com/arrays.schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "description": "Diet preferences",
            "type": "object",
            "additionalProperties": False,
            "patternProperties": {
                "^iLike(Meat|Drinks)$": {
                    "type": "boolean",
                    "description": "Do I like it?",
                },
            },
        }

        expected_output = [
            "# JSON Schema\n\n",
            "*Diet preferences*\n\n",
            "## Pattern Properties\n\n",
            '- <a id="patternProperties"></a>**`^iLike(Meat|Drinks)$`** *(boolean)*: Do I like it?\n',
        ]

        assert expected_output == parser.parse_schema(test_schema)

    def test_parse_top_level_items(self):
        """Test."""
        parser = jsonschema2md.Parser()

        test_schema = {
            "$id": "https://example.com/arrays.schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Fruits",
            "description": "Fruits I like",
            "type": "array",
            "items": {
                "description": "A list of fruits",
                "type": "object",
                "maxProperties": 2,
                "properties": {
                    "name": {"description": "The name of the fruit", "type": "string"},
                    "sweet": {
                        "description": "Whether it is sweet or not",
                        "type": "boolean",
                    },
                },
            },
        }

        expected_output = [
            "# Fruits\n\n",
            "*Fruits I like*\n\n",
            "## Items\n\n",
            '- <a id="items"></a>**Items** *(object)*: A list of fruits. Number of '
            "properties must be at most 2.\n",
            '  - <a id="items/properties/name"></a>**`name`** *(string)*: The name of the fruit.\n',
            '  - <a id="items/properties/sweet"></a>**`sweet`** *(boolean)*: Whether it is sweet or not.\n',
        ]

        assert expected_output == parser.parse_schema(test_schema)

    def test_schema_composition_keywords(self):
        """Test."""
        parser = jsonschema2md.Parser()
        test_schema = {
            "$id": "https://example.com/arrays.schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "description": "Schema composition test case",
            "type": "object",
            "properties": {
                "all_of_example": {
                    "allOf": [
                        {"type": "number"},
                        {"type": "integer"},
                    ],
                },
                "any_of_example": {"anyOf": [{"type": "string"}, {"type": "number", "minimum": 0}]},
                "one_of_example": {
                    "default": [1, 2, 3],
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "items": {"type": "number"}},
                    ],
                },
            },
        }
        expected_output = [
            "# JSON Schema\n\n",
            "*Schema composition test case*\n\n",
            "## Properties\n\n",
            '- <a id="properties/all_of_example"></a>**`all_of_example`**\n',
            "  - **All of**\n",
            '    - <a id="properties/all_of_example/allOf/0"></a>*number*\n',
            '    - <a id="properties/all_of_example/allOf/1"></a>*integer*\n',
            '- <a id="properties/any_of_example"></a>**`any_of_example`**\n',
            "  - **Any of**\n",
            '    - <a id="properties/any_of_example/anyOf/0"></a>*string*\n',
            '    - <a id="properties/any_of_example/anyOf/1"></a>*number*: Minimum: `0`.\n',
            '- <a id="properties/one_of_example"></a>**`one_of_example`**: Default: `[1, 2, 3]`.\n',
            "  - **One of**\n",
            '    - <a id="properties/one_of_example/oneOf/0"></a>*null*\n',
            '    - <a id="properties/one_of_example/oneOf/1"></a>*array*\n',
            '      - <a id="properties/one_of_example/oneOf/1/items"></a>**Items** *(number)*\n',
        ]
        assert expected_output == parser.parse_schema(test_schema)

    def test_pattern_ignore(self):
        test_schema = {
            "type": "object",
            "properties": {
                "general": {
                    "description": "General settings.",
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "pipeline": {
                            "description": "Pipeline to use, depending on input format",
                            "type": "string",
                            "enum": ["infer", "pin", "tandem", "maxquant", "msgfplus", "peptideshaker"],
                            "default": "infer",
                        },
                    },
                },
                "ignoreme": {
                    "description": "Ignored property",
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "thing": {
                            "description": "the description",
                            "type": "string",
                            "enum": ["infer", "pin", "tandem", "maxquant", "msgfplus", "peptideshaker"],
                            "default": "infer",
                        },
                    },
                },
            },
        }
        parser = jsonschema2md.Parser(ignore_patterns=[r".*ignoreme.*"])
        expected_output = [
            "# JSON Schema\n\n",
            "## Properties\n\n",
            '- <a id="properties/general"></a>**`general`** *(object)*: General '
            "settings. Cannot contain additional properties.\n",
            '  - <a id="properties/general/properties/pipeline"></a>**`pipeline`** '
            "*(string)*: Pipeline to use, depending on input format. Must be one of: "
            '`["infer", "pin", "tandem", "maxquant", "msgfplus", "peptideshaker"]`. '
            'Default: `"infer"`.\n',
        ]
        assert expected_output == parser.parse_schema(test_schema)

    def test_collapse_children(self):
        test_schema = {
            "type": "object",
            "properties": {
                "general": {
                    "description": "General settings.",
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "pipeline": {
                            "description": "Pipeline to use, depending on input format",
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "foo": {
                                    "description": "Foo description",
                                    "type": "string",
                                    "enum": [
                                        "infer",
                                        "pin",
                                        "tandem",
                                        "maxquant",
                                        "msgfplus",
                                        "peptideshaker",
                                    ],
                                    "default": "infer",
                                }
                            },
                        },
                    },
                }
            },
        }
        parser = jsonschema2md.Parser(collapse_children=True)
        expected_output = [
            "# JSON Schema\n\n",
            "## Properties\n\n",
            "- <details>",
            "<summary>",
            '<a id="properties/general"></a><strong><code>general</code></strong> '
            "<em>(object)</em>: General settings. Cannot contain additional "
            "properties.",
            "</summary>\n\n",
            "  - <details>",
            "<summary>",
            "<a "
            'id="properties/general/properties/pipeline"></a><strong><code>pipeline</code></strong> '
            "<em>(object)</em>: Pipeline to use, depending on input format. Cannot "
            "contain additional properties.",
            "</summary>\n\n",
            "    - <a "
            'id="properties/general/properties/pipeline/properties/foo"></a>**`foo`** '
            '*(string)*: Foo description. Must be one of: `["infer", "pin", "tandem", '
            '"maxquant", "msgfplus", "peptideshaker"]`. Default: `"infer"`.\n',
            "\n    </details>\n\n",
            "\n  </details>\n\n",
        ]
        assert expected_output == parser.parse_schema(test_schema)
