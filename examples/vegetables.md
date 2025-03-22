# JSON Schema

_Vegetable preferences_

## Properties

- <a id="properties/fruits"></a>**`fruits`** _(array)_
  - <a id="properties/fruits/items"></a>**Items** _(string)_
- <a id="properties/vegetables"></a>**`vegetables`** _(array)_
  - <a id="properties/vegetables/items"></a>**Items**: Refer to _[#/definitions/veggie](#definitions/veggie)_.

## Definitions

- <a id="definitions/veggie"></a>**`veggie`** _(object)_
  - <a id="definitions/veggie/properties/veggieName"></a>**`veggieName`** _(string, required)_: The name of the vegetable.
  - <a id="definitions/veggie/properties/veggieLike"></a>**`veggieLike`** _(boolean, required)_: Do I like this vegetable?
  - <a id="definitions/veggie/properties/type_number"></a>**`type_number`** _(array)_: The type and number of vegetable.
    - **Items**:
      - <a id="definitions/veggie/properties/type_number/items/0"></a>_string_: The type of the vegetable.
      - <a id="definitions/veggie/properties/type_number/items/1"></a>_number_: The number of vegetable.

## Examples

```json
{
  "fruits": ["apple", "orange"],
  "vegetables": [
    {
      "veggieName": "cabbage",
      "veggieLike": true
    }
  ]
}
```
