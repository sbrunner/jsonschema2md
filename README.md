# jsonschema2md

[![](https://flat.badgen.net/pypi/v/jsonschema2md?icon=pypi)](https://pypi.org/project/jsonschema2md)
[![](https://flat.badgen.net/github/release/sbrunner/jsonschema2md)](https://github.com/sbrunner/jsonschema2md/releases)
[![](https://flat.badgen.net/github/checks/sbrunner/jsonschema2md/)](https://github.com/sbrunner/jsonschema2md/actions)
![](https://flat.badgen.net/github/last-commit/sbrunner/jsonschema2md)
![](https://flat.badgen.net/github/license/sbrunner/jsonschema2md)

_Convert JSON Schemas to simple, human-readable Markdown documentation._

---

For example:

```json
{
  "$id": "https://example.com/person.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Person",
  "description": "JSON Schema for a person object.",
  "type": "object",
  "properties": {
    "firstName": {
      "type": "string",
      "description": "The person's first name."
    },
    "lastName": {
      "type": "string",
      "description": "The person's last name."
    }
  }
}
```

will be converted to:

> # Person
>
> _JSON Schema for a person object._
>
> ## Properties
>
> - **`firstName`** _(string)_: The person's first name.
> - **`lastName`** _(string)_: The person's last name.

There's also the possibility to translate it to another language. For example, the same schema in French would result in:

> # Person
>
> _JSON Schema for a person object._
>
> ## Propriétés
>
> - **`firstName`** _(chaîne de caractères)_: The person's first name.
> - **`lastName`** _(chaîne de caractères)_: The person's last name.

See the [examples](https://github.com/sbrunner/jsonschema2md/tree/master/examples)
directory for more elaborate examples.

---

## Installation

Install with pip

```sh
pip install jsonschema2md
```

## Usage

### From the CLI

```sh
jsonschema2md [OPTIONS] <input.json> <output.md>
```

### From Python

```python
import json
import jsonschema2md

parser = jsonschema2md.Parser(
    examples_as_yaml=False,
    show_examples="all",
)
with open("./examples/food.json", "r") as json_file:
    md_lines = parser.parse_schema(json.load(json_file))
print(''.join(md_lines))
```

### Options

- `examples_as_yaml`: Parse examples in YAML-format instead of JSON. (`bool`, default:
  `False`)
- `show_examples`: Parse examples for only the main object, only properties, or all.
  (`str`, default `all`, options: `object`, `properties`, `all`)
- `show_deprecated`: Show deprecated properties. (`bool`, default: `True`)
- `collapse_children`: Collapse object children into a `<details>` element (`bool`, default:
  `False`)
- `header_level`: Base header level for the generated markdown. (`int`, default: `0`)
- `ignore_patterns`: List of regex patterns to ignore when parsing the schema. (`list of
str`, default: `None`)

## pre-commit hook

You can use the pre-commit hook with:

```yaml
repos:
  - repo: https://github.com/sbrunner/jsonschema2md
    rev: <version> # Use the ref you want to point at
    hooks:
      - id: jsonschema2md
        files: schema.json
        args:
          - --pre-commit
          - schema.json
          - schema.md
```

## Contributing

Bugs, questions or suggestions? Feel free to post an issue in the
[issue tracker](https://github.com/sbrunner/jsonschema2md/issues/) or to make a pull
request! See
[Contributing.md](https://github.com/sbrunner/jsonschema2md/blob/master/CONTRIBUTING.md)
for more info.

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```

## Showcase

- [PrairieLearn's `infoCourse.json`](https://prairielearn.readthedocs.io/en/latest/schemas/infoCourse/), [source code](https://github.com/PrairieLearn/PrairieLearn/blob/ab1e0f1fc837a8da9cde3448eb785958ac42e309/docs/scripts/gen_jsonschemas.py).

## Related projects:

- [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans)
- [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown)
- [adobe/jsonschema2md](https://github.com/adobe/jsonschema2md)
