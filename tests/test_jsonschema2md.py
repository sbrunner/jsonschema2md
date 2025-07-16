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
            "## Additional properties\n\n",
            '- <a id="additionalProperties"></a>**Additional properties** *(object)*: '
            "Additional info about foods you may like.\n",
            "  - <a "
            'id="additionalProperties/patternProperties/%5EiLike%28Meat%7CDrinks%29%24"></a>**`^iLike(Meat|Drinks)$`** '
            "*(boolean)*: Do I like it?\n",
            "## Unevaluated properties\n\n",
            '- <a id="unevaluatedProperties"></a>**Unevaluated properties** '
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
        assert expected_output == parser.parse_schema(self.test_schema, locale="en_US")


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
                    'Must be one of: "eggplant", "spinach", or "cabbage". '
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
            {
                "input": {
                    "type": "object",
                    "additionalProperties": {},
                    "properties": {},
                },
                "add_type": False,
                "expected_output": ": Can contain additional properties.",
            },
            {
                "input": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "properties": {},
                },
                "add_type": False,
                "expected_output": ": Can contain additional properties.",
            },
            {
                "input": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {},
                },
                "add_type": False,
                "expected_output": ": Cannot contain additional properties.",
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
            "## Additional properties\n\n",
            '- <a id="additionalProperties"></a>**Additional properties** *(object)*: '
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
            "## Additional properties\n\n",
            '- <a id="additionalProperties"></a>**Additional properties** *(object)*: '
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
        assert expected_output == parser.parse_schema(self.test_schema, locale="en_US")

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

        assert expected_output == parser.parse_schema(test_schema, locale="en_US")

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

        assert expected_output == parser.parse_schema(test_schema, locale="en_US")

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
                "all_of_merged_example": {
                    "allOf": [
                        {"type": "number"},
                    ],
                },
                "any_of_merged_example": {
                    "anyOf": [
                        {"type": "string"},
                    ],
                },
                "one_of_merged_example": {
                    "oneOf": [
                        {"type": "number"},
                    ],
                },
                # Multiple composition keywords
                "bad_merged_example_1": {
                    "allOf": [
                        {"type": "number"},
                    ],
                    "oneOf": [
                        {"type": "string"},
                    ],
                },
                # A merge is possible, but would conflict
                "bad_merged_example_2": {
                    "allOf": [
                        {"type": "number"},
                    ],
                    "type": "string",
                },
                # A merge is possible, and doesn't conflict
                "good_merged_example": {
                    "allOf": [
                        {"type": "number"},
                    ],
                    "type": "number",
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
            '- <a id="properties/all_of_merged_example"></a>**`all_of_merged_example`** *(number)*\n',
            '- <a id="properties/any_of_merged_example"></a>**`any_of_merged_example`** *(string)*\n',
            '- <a id="properties/one_of_merged_example"></a>**`one_of_merged_example`** *(number)*\n',
            '- <a id="properties/bad_merged_example_1"></a>**`bad_merged_example_1`**\n',
            "  - **All of**\n",
            '    - <a id="properties/bad_merged_example_1/allOf/0"></a>*number*\n',
            "  - **One of**\n",
            '    - <a id="properties/bad_merged_example_1/oneOf/0"></a>*string*\n',
            '- <a id="properties/bad_merged_example_2"></a>**`bad_merged_example_2`** *(string)*\n',
            "  - **All of**\n",
            '    - <a id="properties/bad_merged_example_2/allOf/0"></a>*number*\n',
            '- <a id="properties/good_merged_example"></a>**`good_merged_example`** *(number)*\n',
        ]
        assert expected_output == parser.parse_schema(test_schema, locale="en_US")

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
            '"infer", "pin", "tandem", "maxquant", "msgfplus", or "peptideshaker". '
            'Default: `"infer"`.\n',
        ]
        assert expected_output == parser.parse_schema(test_schema, locale="en_US")

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
            '*(string)*: Foo description. Must be one of: "infer", "pin", "tandem", '
            '"maxquant", "msgfplus", or "peptideshaker". Default: `"infer"`.\n',
            "\n    </details>\n\n",
            "\n  </details>\n\n",
        ]
        assert expected_output == parser.parse_schema(test_schema, locale="en_US")

    def test_hide_empty_description(self):
        test_schema = {
            "description": "Arbitrary comment for reference purposes.",
            "id": "CommentJsonSchema",
            "properties": {
                "comment": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "array", "items": {}},
                        {"type": "object", "additionalProperties": {}, "properties": {}},
                    ]
                }
            },
        }
        parser = jsonschema2md.Parser()
        expected_output = [
            "# JSON Schema\n\n",
            "*Arbitrary comment for reference purposes.*\n\n",
            "## Properties\n\n",
            '- <a id="properties/comment"></a>**`comment`**\n',
            "  - **Any of**\n",
            '    - <a id="properties/comment/anyOf/0"></a>*string*\n',
            '    - <a id="properties/comment/anyOf/1"></a>*array*\n',
            '    - <a id="properties/comment/anyOf/2"></a>*object*: Can contain additional properties.\n',
        ]
        assert expected_output == parser.parse_schema(test_schema, locale="en_US")


class TestParserFR:
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
                    ": The name of the vegetable. Doit être de type *string*. "
                    'Doit être l\'un des suivants : "eggplant", "spinach" ou "cabbage". '
                    "Se référer à *[#/definitions/veggies](#definitions/veggies)*. "
                    'Par défaut : `"eggplant"`.'
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
                    ": Number of vegetables. Minimum : `0`. Maximum : `999`. "
                    "Peut contenir des propriétés supplémentaires. Par défaut : `0`."
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
                    ": Number of vegetables. Minimum exclusif : `0`. Maximum exclusif : `1000`. Par défaut : `1`."
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
                    ": List of vegetables. Ne peut pas contenir des propriétés supplémentaires. Par défaut : `[]`."
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
                    ': List of vegetables. La longueur doit être d\'au moins 1. Par défaut : `["Carrot"]`.'
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
                    ': List of vegetables. La longueur doit être au maximum de 10. Par défaut : `["Carrot"]`.'
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
                    "La longueur doit être comprise entre 1 et 10 (inclus). "
                    'Par défaut : `["Carrot"]`.'
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
                    "La longueur doit être égale à 5. "
                    'Par défaut : `["Carrot", "Mushroom", "Cabbage", "Broccoli", "Leek"]`.'
                ),
            },
            {
                "input": {
                    "type": "object",
                    "additionalProperties": {},
                    "properties": {},
                },
                "add_type": False,
                "expected_output": ": Peut contenir des propriétés supplémentaires.",
            },
            {
                "input": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "properties": {},
                },
                "add_type": False,
                "expected_output": ": Peut contenir des propriétés supplémentaires.",
            },
            {
                "input": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {},
                },
                "add_type": False,
                "expected_output": ": Ne peut pas contenir des propriétés supplémentaires.",
            },
        ]

        parser = jsonschema2md.Parser()
        jsonschema2md.Parser.current_locale = "fr"

        for case in test_cases:
            observed_output = " ".join(
                parser._construct_description_line(case["input"], add_type=case["add_type"]),
            )
            assert case["expected_output"] == observed_output

    def test_parse_object(self):
        """Test."""
        parser = jsonschema2md.Parser()
        jsonschema2md.Parser.current_locale = "fr"

        expected_output = [
            '- <a id="properties/fruits"></a>**`fruits`** *(tableau)*\n',
            '  - <a id="properties/fruits/items"></a>**Éléments** *(chaîne de caractères)*\n',
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
            "## Propriétés supplémentaires\n\n",
            '- <a id="additionalProperties"></a>**Propriétés supplémentaires** *(objet)*: '
            "Additional info about foods you may like.\n",
            "  - <a "
            'id="additionalProperties/patternProperties/%5EiLike%28Meat%7CDrinks%29%24"></a>**`^iLike(Meat|Drinks)$`** '
            "*(booléen)*: Do I like it?\n",
            "## Propriétés\n\n",
            '- <a id="properties/fruits"></a>**`fruits`** *(tableau)*\n',
            '  - <a id="properties/fruits/items"></a>**Éléments** *(chaîne de caractères)*\n',
            '- <a id="properties/vegetables"></a>**`vegetables`** *(tableau)*\n',
            '  - <a id="properties/vegetables/items"></a>**Éléments**: Se référer à '
            "*[#/definitions/veggie](#definitions/veggie)*.\n",
            '- <a id="properties/cakes"></a>**`cakes`** *(tableau)*: Le schéma « contains » '
            "doit correspondre au maximum 3 fois.\n",
            '  - <a id="properties/cakes/contains"></a>**Contient**: Se référer à '
            "*[#/definitions/cake](#definitions/cake)*.\n",
            "## Définitions\n\n",
            '- <a id="definitions/veggie"></a>**`veggie`** *(objet)*\n',
            '  - <a id="definitions/veggie/properties/veggieName"></a>**`veggieName`** '
            "*(chaîne de caractères, obligatoire)*: The name of the vegetable.\n",
            '  - <a id="definitions/veggie/properties/veggieLike"></a>**`veggieLike`** '
            "*(booléen, obligatoire)*: Do I like this vegetable?\n",
            '  - <a id="definitions/veggie/properties/expiresAt"></a>**`expiresAt`** '
            "*(chaîne de caractères, format : date, obligatoire <sub><sup>si `veggieLike` est "
            "défini</sup></sub>)*: When does the veggie expires.\n",
            '- <a id="definitions/cake"></a>**`cake`** *(chaîne de caractères)*: A cake.\n',
            "## Exemples\n\n",
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
        assert expected_output == parser.parse_schema(self.test_schema, locale="fr")

    def test_parse_schema_examples_yaml(self):
        """Test."""
        parser = jsonschema2md.Parser(examples_as_yaml=True)
        expected_output = [
            "# JSON Schema\n\n",
            "*Food preferences*\n\n",
            "## Propriétés supplémentaires\n\n",
            '- <a id="additionalProperties"></a>**Propriétés supplémentaires** *(objet)*: '
            "Additional info about foods you may like.\n",
            "  - <a "
            'id="additionalProperties/patternProperties/%5EiLike%28Meat%7CDrinks%29%24"></a>**`^iLike(Meat|Drinks)$`** '
            "*(booléen)*: Do I like it?\n",
            "## Propriétés\n\n",
            '- <a id="properties/fruits"></a>**`fruits`** *(tableau)*\n',
            '  - <a id="properties/fruits/items"></a>**Éléments** *(chaîne de caractères)*\n',
            '- <a id="properties/vegetables"></a>**`vegetables`** *(tableau)*\n',
            '  - <a id="properties/vegetables/items"></a>**Éléments**: Se référer à '
            "*[#/definitions/veggie](#definitions/veggie)*.\n",
            '- <a id="properties/cakes"></a>**`cakes`** *(tableau)*: Le schéma « contains » '
            "doit correspondre au maximum 3 fois.\n",
            '  - <a id="properties/cakes/contains"></a>**Contient**: Se référer à '
            "*[#/definitions/cake](#definitions/cake)*.\n",
            "## Définitions\n\n",
            '- <a id="definitions/veggie"></a>**`veggie`** *(objet)*\n',
            '  - <a id="definitions/veggie/properties/veggieName"></a>**`veggieName`** '
            "*(chaîne de caractères, obligatoire)*: The name of the vegetable.\n",
            '  - <a id="definitions/veggie/properties/veggieLike"></a>**`veggieLike`** '
            "*(booléen, obligatoire)*: Do I like this vegetable?\n",
            '  - <a id="definitions/veggie/properties/expiresAt"></a>**`expiresAt`** '
            "*(chaîne de caractères, format : date, obligatoire <sub><sup>si `veggieLike` est "
            "défini</sup></sub>)*: When does the veggie expires.\n",
            '- <a id="definitions/cake"></a>**`cake`** *(chaîne de caractères)*: A cake.\n',
            "## Exemples\n\n",
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
        assert expected_output == parser.parse_schema(self.test_schema, locale="fr")

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
            "## Propriétés supplémentaires\n\n",
            '- <a id="patternProperties"></a>**`^iLike(Meat|Drinks)$`** *(booléen)*: Do I like it?\n',
        ]

        assert expected_output == parser.parse_schema(test_schema, locale="fr")

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
            "## Éléments\n\n",
            '- <a id="items"></a>**Éléments** *(objet)*: A list of fruits. Le nombre de '
            "propriétés doit être au maximum de 2.\n",
            '  - <a id="items/properties/name"></a>**`name`** *(chaîne de caractères)*: The name of the fruit.\n',
            '  - <a id="items/properties/sweet"></a>**`sweet`** *(booléen)*: Whether it is sweet or not.\n',
        ]

        assert expected_output == parser.parse_schema(test_schema, locale="fr")

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
                "all_of_merged_example": {
                    "allOf": [
                        {"type": "number"},
                    ],
                },
                "any_of_merged_example": {
                    "anyOf": [
                        {"type": "string"},
                    ],
                },
                "one_of_merged_example": {
                    "oneOf": [
                        {"type": "number"},
                    ],
                },
                # Multiple composition keywords
                "bad_merged_example_1": {
                    "allOf": [
                        {"type": "number"},
                    ],
                    "oneOf": [
                        {"type": "string"},
                    ],
                },
                # A merge is possible, but would conflict
                "bad_merged_example_2": {
                    "allOf": [
                        {"type": "number"},
                    ],
                    "type": "string",
                },
                # A merge is possible, and doesn't conflict
                "good_merged_example": {
                    "allOf": [
                        {"type": "number"},
                    ],
                    "type": "number",
                },
            },
        }

        expected_output = [
            "# JSON Schema\n\n",
            "*Schema composition test case*\n\n",
            "## Propriétés\n\n",
            '- <a id="properties/all_of_example"></a>**`all_of_example`**\n',
            "  - **Tous les**\n",
            '    - <a id="properties/all_of_example/allOf/0"></a>*nombre*\n',
            '    - <a id="properties/all_of_example/allOf/1"></a>*entier*\n',
            '- <a id="properties/any_of_example"></a>**`any_of_example`**\n',
            "  - **Un des**\n",
            '    - <a id="properties/any_of_example/anyOf/0"></a>*chaîne de caractères*\n',
            '    - <a id="properties/any_of_example/anyOf/1"></a>*nombre*: Minimum : `0`.\n',
            '- <a id="properties/one_of_example"></a>**`one_of_example`**: Par défaut : `[1, 2, 3]`.\n',
            "  - **L'un de**\n",
            '    - <a id="properties/one_of_example/oneOf/0"></a>*null*\n',
            '    - <a id="properties/one_of_example/oneOf/1"></a>*tableau*\n',
            '      - <a id="properties/one_of_example/oneOf/1/items"></a>**Éléments** *(nombre)*\n',
            '- <a id="properties/all_of_merged_example"></a>**`all_of_merged_example`** *(nombre)*\n',
            '- <a id="properties/any_of_merged_example"></a>**`any_of_merged_example`** *(chaîne de caractères)*\n',
            '- <a id="properties/one_of_merged_example"></a>**`one_of_merged_example`** *(nombre)*\n',
            '- <a id="properties/bad_merged_example_1"></a>**`bad_merged_example_1`**\n',
            "  - **Tous les**\n",
            '    - <a id="properties/bad_merged_example_1/allOf/0"></a>*nombre*\n',
            "  - **L'un de**\n",
            '    - <a id="properties/bad_merged_example_1/oneOf/0"></a>*chaîne de caractères*\n',
            '- <a id="properties/bad_merged_example_2"></a>**`bad_merged_example_2`** *(chaîne de caractères)*\n',
            "  - **Tous les**\n",
            '    - <a id="properties/bad_merged_example_2/allOf/0"></a>*nombre*\n',
            '- <a id="properties/good_merged_example"></a>**`good_merged_example`** *(nombre)*\n',
        ]

        assert expected_output == parser.parse_schema(test_schema, locale="fr")

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
            "## Propriétés\n\n",
            '- <a id="properties/general"></a>**`general`** *(objet)*: General '
            "settings. Ne peut pas contenir des propriétés supplémentaires.\n",
            '  - <a id="properties/general/properties/pipeline"></a>**`pipeline`** '
            "*(chaîne de caractères)*: Pipeline to use, depending on input format. "
            'Doit être l\'un des suivants : "infer", "pin", "tandem", "maxquant", '
            '"msgfplus" ou "peptideshaker". Par défaut : `"infer"`.\n',
        ]
        assert expected_output == parser.parse_schema(test_schema, locale="fr")

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
            "## Propriétés\n\n",
            "- <details>",
            "<summary>",
            '<a id="properties/general"></a><strong><code>general</code></strong> '
            "<em>(objet)</em>: General settings. Ne peut pas contenir des propriétés "
            "supplémentaires.",
            "</summary>\n\n",
            "  - <details>",
            "<summary>",
            "<a "
            'id="properties/general/properties/pipeline"></a><strong><code>pipeline</code></strong> '
            "<em>(objet)</em>: Pipeline to use, depending on input format. Ne peut pas "
            "contenir des propriétés supplémentaires.",
            "</summary>\n\n",
            "    - <a "
            'id="properties/general/properties/pipeline/properties/foo"></a>**`foo`** '
            "*(chaîne de caractères)*: Foo description. Doit être l'un des suivants : "
            '"infer", "pin", "tandem", "maxquant", "msgfplus" ou "peptideshaker". '
            'Par défaut : `"infer"`.\n',
            "\n    </details>\n\n",
            "\n  </details>\n\n",
        ]
        assert expected_output == parser.parse_schema(test_schema, locale="fr")

    def test_hide_empty_description(self):
        test_schema = {
            "description": "Arbitrary comment for reference purposes.",
            "id": "CommentJsonSchema",
            "properties": {
                "comment": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "array", "items": {}},
                        {"type": "object", "additionalProperties": {}, "properties": {}},
                    ]
                }
            },
        }
        parser = jsonschema2md.Parser()
        expected_output = [
            "# JSON Schema\n\n",
            "*Arbitrary comment for reference purposes.*\n\n",
            "## Propriétés\n\n",
            '- <a id="properties/comment"></a>**`comment`**\n',
            "  - **Un des**\n",
            '    - <a id="properties/comment/anyOf/0"></a>*chaîne de caractères*\n',
            '    - <a id="properties/comment/anyOf/1"></a>*tableau*\n',
            '    - <a id="properties/comment/anyOf/2"></a>*objet*: Peut contenir des propriétés supplémentaires.\n',
        ]

        assert expected_output == parser.parse_schema(test_schema, locale="fr")
