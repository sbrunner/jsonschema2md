"""Convert JSON Schema to Markdown documentation."""

__author__ = "Stéphane Brunner"
__email__ = "stephane.brunner@gmail.com"
__license__ = "Apache-2.0"


try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

import argparse
import gettext
import io
import json
import re
import subprocess  # nosec
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any, Literal, Optional, Union
from urllib.parse import quote

import markdown
import yaml
from babel import default_locale, negotiate_locale
from babel.lists import format_list
from babel.support import LazyProxy

__version__ = version("jsonschema2md")
_translations_cache: dict[str, gettext.GNUTranslations] = {}


def get_locales() -> tuple[str, ...]:
    """Get the list of available locales."""
    languages = (Path(__file__).parent / "locales").glob("*/LC_MESSAGES/messages.mo")
    languages = (p.parent.parent for p in languages)

    return ("en", "en_US", *sorted(lang.name for lang in languages))


def _(message: str) -> str:
    """Translate a message using gettext."""
    if Parser.current_locale is None or Parser.current_locale in ("en", "en_US"):
        return message

    if not _translations_cache.get(Parser.current_locale):
        _translations_cache[Parser.current_locale] = gettext.translation(
            "messages",
            localedir=str(Path(__file__).parent / "locales"),
            languages=[Parser.current_locale],
        )
    return _translations_cache[Parser.current_locale].gettext(message)


def t(message: str) -> LazyProxy:
    """Translate a message using gettext only when it's used."""
    return LazyProxy(_, message, enable_cache=False)


def _maybe_list(
    obj: Union[list[str], str],
    style: Literal[
        "standard",
        "standard-short",
        "or",
        "or-short",
        "unit",
        "unit-short",
        "unit-narrow",
    ] = "standard",
    mapper: Callable[[str], str] = lambda x: x,
) -> str:
    """Format a list of strings or a single string."""
    if isinstance(obj, list):
        if len(obj) == 0:
            return "[]"
        return _format_list((mapper(x) for x in obj), style=style)
    return mapper(obj)


def _format_list(
    iter_: Iterable[str],
    style: Literal[
        "standard",
        "standard-short",
        "or",
        "or-short",
        "unit",
        "unit-short",
        "unit-narrow",
    ] = "standard",
    locale: Optional[str] = None,
) -> str:
    if locale is None:
        locale = Parser.current_locale

    # Prune falsy values.
    iter_ = filter(None, iter_)

    return format_list(tuple(iter_), style, locale)


PROPERTY_NAMES = {
    "items": t("Items"),
    "contains": t("Contains"),
    "definitions": t("Definitions"),
    "$defs": "$defs",
}

TYPES = {
    "array": t("array"),
    "boolean": t("boolean"),
    "null": t("null"),
    "integer": t("integer"),
    "number": t("number"),
    "object": t("object"),
    "string": t("string"),
}


class Parser:
    """
    JSON Schema to Markdown parser.

    Examples
    --------
    >>> import jsonschema2md
    >>> parser = jsonschema2md.Parser()
    >>> md_lines = parser.parse_schema(json.load(input_json))
    """

    tab_size = 2
    current_locale: Optional[str] = None

    def __init__(
        self,
        examples_as_yaml: bool = False,
        show_examples: str = "all",
        show_deprecated: bool = False,
        collapse_children: bool = False,
        header_level: int = 0,
        ignore_patterns: Optional[Sequence[str]] = None,
    ) -> None:
        """
        Initialize JSON Schema to Markdown parser.

        Parameters
        ----------
        examples_as_yaml : bool, default False
            Parse examples in YAML-format instead of JSON.
        show_examples: str, default 'all'
            Parse examples for only objects, only properties or all. Valid options are
            `{"all", "object", "properties"}`.
        show_deprecated : bool, default False
            If `True`, includes deprecated properties in the generated markdown. This
            allows for documenting properties that are no longer recommended for use.
        collapse_children : bool, default False
            If `True`, collapses objects with children in the generated markdown. This
            allows for a cleaner view of the schema.
        header_level : int, default 0
            Base header level for the generated markdown. This is useful to include the
            generated markdown in a larger document with its own header levels.
        ignore_patterns : list of str, default None
            List of regex patterns to ignore when parsing the schema. This can be useful
            to skip certain properties or definitions that are not relevant for the
            documentation. The patterns are matched against the full path of the
            property or definition (e.g., `properties/name`, `definitions/Person`).

        """
        self.examples_as_yaml = examples_as_yaml
        self.show_deprecated = show_deprecated
        self.header_level = header_level
        self.collapse_children = collapse_children
        self.ignore_patterns = ignore_patterns if ignore_patterns else []

        valid_show_examples_options = ["all", "object", "properties"]
        show_examples = show_examples.lower()
        if show_examples in valid_show_examples_options:
            self.show_examples = show_examples
        else:
            message = (
                f"`show_examples` option should be one of "
                f"`{valid_show_examples_options}`; `{show_examples}` was passed.",
            )
            raise ValueError(message)

    def _construct_description_line(self, obj: dict[str, Any], add_type: bool = False) -> Sequence[str]:
        """Construct description line of property, definition, or item."""
        description_line = []

        if "description" in obj:
            ending = "" if re.search(r"[.?!;]$", obj["description"]) else "."
            description_line.append(f"{obj['description']}{ending}")
        if add_type and "type" in obj:
            description_line.append(_("Must be of type *%(type)s*.") % {"type": obj["type"]})
        if "contentEncoding" in obj:
            description_line.append(
                _("Content encoding: `%(encoding)s`.") % {"encoding": obj["contentEncoding"]},
            )
        if "contentMediaType" in obj:
            description_line.append(_("Content media type: `%(type)s`.") % {"type": obj["contentMediaType"]})
        if "minimum" in obj:
            description_line.append(_("Minimum: `%(min)d`.") % {"min": obj["minimum"]})
        if "exclusiveMinimum" in obj:
            description_line.append(_("Exclusive minimum: `%(exmin)d`.") % {"exmin": obj["exclusiveMinimum"]})
        if "maximum" in obj:
            description_line.append(_("Maximum: `%(max)d`.") % {"max": obj["maximum"]})
        if "exclusiveMaximum" in obj:
            description_line.append(_("Exclusive maximum: `%(exmax)d`.") % {"exmax": obj["exclusiveMaximum"]})
        if "minItems" in obj or "maxItems" in obj:
            if "minItems" in obj and "maxItems" not in obj:
                length_description = _("Length must be at least %(min)d.") % {"min": obj["minItems"]}
            elif "maxItems" in obj and "minItems" not in obj:
                length_description = _("Length must be at most %(max)d.") % {"max": obj["maxItems"]}
            elif obj["minItems"] == obj["maxItems"]:
                length_description = _("Length must be equal to %(length)d.") % {"length": obj["minItems"]}
            else:
                length_description = _("Length must be between %(min)d and %(max)d (inclusive).") % {
                    "min": obj["minItems"],
                    "max": obj["maxItems"],
                }
            description_line.append(length_description)
        if "multipleOf" in obj:
            if obj["multipleOf"] == 1:
                description_line.append(_("Must be an integer."))
            else:
                description_line.append(
                    _("Must be a multiple of `%(multiple)d`.") % {"multiple": obj["multipleOf"]},
                )

        if "minLength" in obj or "maxLength" in obj:
            if "minLength" in obj and "maxLength" not in obj:
                length_description = _("Length must be at least %(min)d.") % {"min": obj["minLength"]}
            elif "maxLength" in obj and "minLength" not in obj:
                length_description = _("Length must be at most %(max)d.") % {"max": obj["maxLength"]}
            elif obj["minLength"] == obj["maxLength"]:
                length_description = _("Length must be equal to %(length)d.") % {"length": obj["minLength"]}
            else:
                length_description = _("Length must be between %(min)d and %(max)d (inclusive).") % {
                    "min": obj["minLength"],
                    "max": obj["maxLength"],
                }
            description_line.append(length_description)
        if "pattern" in obj:
            link = f"https://regexr.com/?expression={quote(obj['pattern'])}"
            description_line.append(
                _("Must match pattern: `%(pattern)s` ([Test](%(link)s)).")
                % {
                    "pattern": obj["pattern"],
                    "link": link,
                },
            )
        if obj.get("uniqueItems"):
            description_line.append(_("Items must be unique."))
        if "minContains" in obj or "maxContains" in obj:
            if "minContains" in obj and "maxContains" not in obj:
                contains_description = _("Contains schema must be matched at least %(min)d times.") % {
                    "min": obj["minContains"],
                }
            elif "maxContains" in obj and "minContains" not in obj:
                contains_description = _("Contains schema must be matched at most %(max)d times.") % {
                    "max": obj["maxContains"],
                }
            elif obj["minContains"] == obj["maxContains"]:
                contains_description = _("Contains schema must be matched exactly %(count)d times.") % {
                    "count": obj["minContains"],
                }
            else:
                contains_description = _(
                    "Contains schema must be matched between %(min)d and %(max)d times (inclusive).",
                ) % {
                    "min": obj["minContains"],
                    "max": obj["maxContains"],
                }
            description_line.append(contains_description)
        if "maxProperties" in obj or "minProperties" in obj:
            if "minProperties" in obj and "maxProperties" not in obj:
                properties_description = _("Number of properties must be at least %(min)d.") % {
                    "min": obj["minProperties"],
                }
            elif "maxProperties" in obj and "minProperties" not in obj:
                properties_description = _("Number of properties must be at most %(max)d.") % {
                    "max": obj["maxProperties"],
                }
            elif obj["minProperties"] == obj["maxProperties"]:
                properties_description = _("Number of properties must be equal to %(count)d.") % {
                    "count": obj["minProperties"],
                }
            else:
                properties_description = _(
                    "Number of properties must be between %(min)d and %(max)d (inclusive).",
                ) % {
                    "min": obj["minProperties"],
                    "max": obj["maxProperties"],
                }
            description_line.append(properties_description)
        if "enum" in obj:
            description_line.append(
                _("Must be one of: %(enum)s.")
                % {"enum": _format_list(map(json.dumps, obj["enum"]), style="or")},
            )
        if "const" in obj:
            description_line.append(_("Must be: `%(const)s`.") % {"const": json.dumps(obj["const"])})
        if "additionalProperties" in obj:
            # `False` has different behavior than `{}`.
            if obj["additionalProperties"] is not False:
                description_line.append(_("Can contain additional properties."))
            else:
                description_line.append(_("Cannot contain additional properties."))

        if "unevaluatedProperties" in obj:
            if obj["unevaluatedProperties"] is not False:
                description_line.append(_("Can contain unevaluated properties."))
            else:
                description_line.append(_("Cannot contain unevaluated properties."))

        if "$ref" in obj:
            description_line.append(
                _("Refer to *[%(ref)s](#%(ref_link)s)*.")
                % {"ref": obj["$ref"], "ref_link": quote(obj["$ref"][2:])},
            )
        if "default" in obj:
            description_line.append(_("Default: `%(default)s`.") % {"default": json.dumps(obj["default"])})

        # Only add start colon if items were added
        if description_line:
            description_line.insert(0, ":")

        return description_line

    def _construct_examples(
        self,
        obj: dict[str, Any],
        indent_level: int = 0,
        add_header: bool = True,
    ) -> Sequence[str]:
        def dump_json_with_line_head(obj: dict[str, Any], line_head: str, **kwargs: Any) -> str:
            result = [line_head + line for line in io.StringIO(json.dumps(obj, **kwargs)).readlines()]
            return "".join(result)

        def dump_yaml_with_line_head(obj: dict[str, Any], line_head: str, **kwargs: Any) -> str:
            result = [
                line_head + line
                for line in io.StringIO(yaml.dump(obj, sort_keys=False, **kwargs)).readlines()
            ]
            return "".join(result).rstrip()

        example_lines = []
        if "examples" in obj:
            example_indentation = " " * self.tab_size * (indent_level + 1)
            if add_header:
                example_lines.append(f"\n{example_indentation}{_('Examples:')}\n")
            for example in obj["examples"]:
                if self.examples_as_yaml:
                    lang = "yaml"
                    dump_fn = dump_yaml_with_line_head
                else:
                    lang = "json"
                    dump_fn = dump_json_with_line_head
                example_str = dump_fn(example, line_head=example_indentation, indent=4)
                example_lines.append(
                    f"{example_indentation}```{lang}\n{example_str}\n{example_indentation}```\n\n",
                )
        return example_lines

    def _parse_object(
        self,
        obj: Union[dict[str, Any], list[Any]],
        name: Optional[str],
        path: list[str],
        name_monospace: bool = True,
        output_lines: Optional[list[str]] = None,
        indent_level: int = 0,
        required: bool = False,
        dependent_required: Optional[list[str]] = None,
    ) -> list[str]:
        """Parse JSON object and its items, definitions, and properties recursively."""
        if not output_lines:
            output_lines = []

        indentation = " " * self.tab_size * indent_level
        indentation_items = " " * self.tab_size * (indent_level + 1)

        if isinstance(obj, list):
            output_lines.append(f"{indentation}- **{name}**:\n")

            for i, element in enumerate(obj):
                output_lines = self._parse_object(
                    element,
                    path=[*path, str(i)],
                    name=None,
                    name_monospace=False,
                    output_lines=output_lines,
                    indent_level=indent_level + 2,
                )
            return output_lines

        if not isinstance(obj, dict):
            message = f"Non-object type found in properties list: `{name}: {obj}`."
            raise TypeError(message)

        # If the schema contains a single allOf, anyOf, or oneOf schema,
        # we can lift that schema to the top level if no other properties conflicted.
        # This is particularly useful when the JSON Schema was generated by a tool
        # that outputs this format, e.g. Zod 4.
        schema_composition_keywords = ["allOf", "anyOf", "oneOf"]
        matching_data_len = sum(len(obj.get(k, [])) for k in schema_composition_keywords)
        if matching_data_len == 1:
            for keyword in schema_composition_keywords:
                if keyword in obj:
                    subschema = obj[keyword][0]
                    # Check that no properties conflict with the base object
                    has_subschema_conflict = any(k in subschema and subschema[k] != v for k, v in obj.items())
                    if not has_subschema_conflict:
                        obj = {**subschema, **obj}
                        del obj[keyword]
                        break

        # Construct full description line
        description_line_base = self._construct_description_line(obj)
        description_line_list = [
            line.replace("\n\n", "<br>" + indentation_items) for line in description_line_base
        ]

        # Add full line to output
        description_line = " ".join(description_line_list)
        obj_attributes = []
        formatted_type = ""

        if "type" in obj:
            formatted_type = _maybe_list(obj["type"], style="or", mapper=lambda x: str(TYPES[x]))

        # TL: I'm looking to always have a comma between (type or format) and attributes,
        # so I'm adding them manually.
        optional_format = _(", format: %(format)s") % {"format": obj["format"]} if "format" in obj else ""
        if name is None:
            obj_type = f"*{formatted_type}{optional_format}*" if "type" in obj else ""
            name_formatted = ""
        else:
            obj_attributes.append(_("required") if required else "")
            if dependent_required and not required:
                dependent_required_code = _format_list([f"`{k}`" for k in dependent_required], style="or")
                obj_attributes.append(
                    _("required <sub><sup>if %(dependent)s is set</sup></sub>")
                    % {"dependent": dependent_required_code},
                )

            obj_attributes.extend(
                (
                    _("deprecated") if obj.get("deprecated") else "",
                    _("read-only") if obj.get("readOnly") else "",
                    _("write-only") if obj.get("writeOnly") else "",
                ),
            )

            attributes = (
                _(", %(attributes)s") % {"attributes": _format_list(obj_attributes)}
                if any(obj_attributes)
                else ""
            )

            obj_type = ""
            if "type" in obj:
                obj_type = f" *({formatted_type}{optional_format}{attributes})*"
            elif "$ref" in obj and any(obj_attributes):
                obj_type = f" *({_format_list(obj_attributes)})*"

            name_formatted = f"**`{name}`**" if name_monospace else f"**{name}**"

        has_collapsible_children = any(
            prop in obj and isinstance(obj[prop], dict)
            for prop in [
                "additionalProperties",
                "unevaluatedProperties",
                "properties",
                "patternProperties",
            ]
        )

        has_children = has_collapsible_children or any(
            prop in obj for prop in ["items", "contains", "definitions", "$defs", "anyOf", "oneOf", "allOf"]
        )

        anchor = f'<a id="{quote("/".join(path))}"></a>'
        ignored = any(re.match(ignore, "/".join(path)) is not None for ignore in self.ignore_patterns)
        if obj.get("deprecated") and not self.show_deprecated:
            # Don't even parse children of deprecated properties
            return output_lines

        # In some cases, this description is empty and provides no information,
        # e.g. for `items: {}` or `additionalProperties: {}`.
        # If the description is empty, don't add it.
        description_content = obj_type + description_line.strip()
        show_description = len(description_content) > 0 or has_children

        if not ignored and show_description:
            if has_collapsible_children and self.collapse_children:
                # Expandable children
                output_lines.extend(
                    [
                        f"{indentation}- <details>",
                        "<summary>",
                        markdown.markdown(  # Only HTML is supported for the summary
                            f"{anchor}{name_formatted}{description_content}",
                        )[3:-4],  # Remove <p> tags
                        "</summary>\n\n",
                    ],
                )

            else:
                output_lines.append(
                    f"{indentation}- {anchor}{name_formatted}{description_content}\n",
                )

        # Recursively parse subschemas following schema composition keywords
        schema_composition_keyword_map = {
            "allOf": _("All of"),
            "anyOf": _("Any of"),
            "oneOf": _("One of"),
        }
        for key, label in schema_composition_keyword_map.items():
            if key in obj:
                # Only add if the subschema is not ignored
                ignored_child = any(
                    re.match(ignore, "/".join([*path, key])) is not None for ignore in self.ignore_patterns
                )
                if not ignored_child:
                    output_lines.append(
                        f"{indentation_items}- **{label}**\n",
                    )
                for i, child_obj in enumerate(obj[key]):
                    output_lines = self._parse_object(
                        child_obj,
                        path=[*path, key, str(i)],
                        name=None,
                        name_monospace=False,
                        output_lines=output_lines,
                        indent_level=indent_level + 2,
                    )

        # Recursively add items and definitions
        for property_name in ["items", "contains", "definitions", "$defs"]:
            if property_name in obj:
                output_lines = self._parse_object(
                    obj[property_name],
                    path=[*path, property_name],
                    name=str(PROPERTY_NAMES[property_name]),
                    name_monospace=False,
                    output_lines=output_lines,
                    indent_level=indent_level + 1,
                )

        # Recursively add additional child properties
        for extra_props in ["additional", "unevaluated"]:
            property_name = f"{extra_props}Properties"
            if property_name in obj and isinstance(obj[property_name], dict):
                output_lines = self._parse_object(
                    obj[property_name],
                    path=[*path, property_name],
                    name=_("Additional properties")
                    if extra_props == "additional"
                    else _("Unevaluated properties"),
                    name_monospace=False,
                    output_lines=output_lines,
                    indent_level=indent_level + 1,
                )

        # Recursively add child properties
        for property_name in ["properties", "patternProperties"]:
            if property_name in obj:
                for obj_property_name, property_obj in obj[property_name].items():
                    output_lines = self._parse_object(
                        property_obj,
                        path=[*path, property_name, obj_property_name],
                        name=obj_property_name,
                        output_lines=output_lines,
                        indent_level=indent_level + 1,
                        required=obj_property_name in obj.get("required", []),
                        dependent_required=[
                            k for k, v in obj.get("dependentRequired", {}).items() if obj_property_name in v
                        ],
                    )

        if not ignored and has_collapsible_children and self.collapse_children and show_description:
            output_lines.append(f"\n{indentation_items}</details>\n\n")
        # Add examples
        if self.show_examples in ["all", "properties"]:
            output_lines.extend(self._construct_examples(obj, indent_level=indent_level))

        return output_lines

    def parse_schema(
        self,
        schema_object: dict[str, Any],
        fail_on_error_in_defs: bool = True,
        locale: Optional[str] = None,
    ) -> Sequence[str]:
        """
        Parse JSON Schema object to markdown text.

        Parameters
        ----------
        schema_object: The JSON Schema object to parse.
        fail_on_error_in_defs: If True, the method will raise an error when encountering issues in the
            "definitions" section of the schema. If False, the method will attempt to continue parsing
            despite such errors.

        Returns
        -------
            A list of strings representing the parsed Markdown documentation.
        """
        if locale is not None:
            Parser.current_locale = negotiate_locale((locale,), get_locales())

        output_lines = []

        # Add title and description
        if "title" in schema_object:
            output_lines.append(f"{'#' * (self.header_level + 1)} {schema_object['title']}\n\n")
        else:
            output_lines.append(f"{'#' * (self.header_level + 1)} {_('JSON Schema')}\n\n")
        if "description" in schema_object:
            output_lines.append(f"*{schema_object['description']}*\n\n")

        # Add items
        if "items" in schema_object:
            output_lines.append(f"#{'#' * (self.header_level + 1)} {_('Items')}\n\n")
            output_lines.extend(
                self._parse_object(
                    schema_object["items"],
                    path=["items"],
                    name=_("Items"),
                    name_monospace=False,
                ),
            )

        # Add additional/unevaluated properties
        for extra_props in ["additional", "unevaluated"]:
            property_name = f"{extra_props}Properties"
            title_ = (
                _("Additional properties") if extra_props == "additional" else _("Unevaluated properties")
            )
            if property_name in schema_object and isinstance(schema_object[property_name], dict):
                output_lines.append(f"#{'#' * (self.header_level + 1)} {title_}\n\n")
                output_lines.extend(
                    self._parse_object(
                        schema_object[property_name],
                        path=[property_name],
                        name=title_,
                        name_monospace=False,
                    ),
                )

        # Add pattern properties
        if "patternProperties" in schema_object:
            output_lines.append(f"#{'#' * (self.header_level + 1)} {_('Pattern Properties')}\n\n")
            for obj_name, obj in schema_object["patternProperties"].items():
                output_lines.extend(self._parse_object(obj, path=["patternProperties"], name=obj_name))

        # Add properties
        if "properties" in schema_object:
            output_lines.append(f"#{'#' * (self.header_level + 1)} {_('Properties')}\n\n")
            for obj_name, obj in schema_object["properties"].items():
                required = obj_name in schema_object.get("required", [])
                output_lines.extend(
                    self._parse_object(
                        obj,
                        path=["properties", obj_name],
                        name=obj_name,
                        required=required,
                        dependent_required=[
                            k for k, v in schema_object.get("dependentRequired", {}).items() if obj_name in v
                        ],
                    ),
                )

        # Add definitions / $defs
        for name in ["definitions", "$defs"]:
            if name in schema_object:
                output_lines.append(f"#{'#' * (self.header_level + 1)} {_('Definitions')}\n\n")
                for obj_name, obj in schema_object[name].items():
                    try:
                        output_lines.extend(self._parse_object(obj, path=[name, obj_name], name=obj_name))
                    except Exception as exception:  # pylint: disable=broad-exception-caught
                        message = f"Error parsing {obj_name} from {name} in schema, usually it occurs when the kind of def is not supported."
                        if fail_on_error_in_defs:
                            raise ValueError(message) from exception
                        print(f"WARN: {message}")

        # Add examples
        if "examples" in schema_object and self.show_examples in ["all", "object"]:
            output_lines.append(f"#{'#' * (self.header_level + 1)} {_('Examples')}\n\n")
            output_lines.extend(self._construct_examples(schema_object, indent_level=0, add_header=False))

        Parser.current_locale = None

        return output_lines


def main() -> None:
    """Convert JSON Schema to Markdown documentation."""
    argparser = argparse.ArgumentParser("Convert JSON Schema to Markdown documentation.")
    argparser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    argparser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Run as pre-commit hook after the generation.",
    )
    argparser.add_argument(
        "--examples-as-yaml",
        action="store_true",
        help="Parse examples in YAML-format instead of JSON.",
    )
    argparser.add_argument(
        "--show-examples",
        choices=["all", "properties", "object"],
        default="all",
        help="Parse examples for only the main object, only properties, or all.",
    )
    argparser.add_argument(
        "--header-level",
        type=int,
        default=0,
        help="Base header level for the generated markdown.",
    )
    argparser.add_argument(
        "--ignore_error_in_defs",
        action="store_false",
        dest="fail_on_error_in_defs",
        default=True,
        help="Ignore errors in definitions.",
    )

    argparser.add_argument(
        "--locale",
        choices=get_locales(),
        default=None,
        help="Locale for the output Markdown. If not set, defaults to the first of $LANGUAGE, $LC_ALL, $LC_CTYPE, and $LANG.",
    )
    argparser.add_argument("input_json", type=Path, help="Input JSON file.")
    argparser.add_argument("output_markdown", type=Path, help="Output Markdown file.")

    args = argparser.parse_args()

    if args.locale is None:
        env_locale = default_locale() or "en_US"

        if env_locale not in get_locales():
            old_locale = env_locale
            env_locale = (
                negotiate_locale((env_locale, env_locale.split("_", maxsplit=1)[0]), get_locales()) or "en_US"
            )

            print(
                f"WARNING: The environment's locale `{old_locale}` is not supported, defaulting to `{env_locale}`.",
            )

        args.locale = env_locale

    parser = Parser(
        examples_as_yaml=args.examples_as_yaml,
        show_examples=args.show_examples,
        header_level=args.header_level,
    )
    with args.input_json.open(encoding="utf-8") as input_json:
        output_md = parser.parse_schema(json.load(input_json), args.fail_on_error_in_defs, locale=args.locale)

    with args.output_markdown.open("w", encoding="utf-8") as output_markdown:
        output_markdown.writelines(output_md)

    if args.pre_commit:
        subprocess.run(  # pylint: disable=subprocess-run-check # nosec
            ["pre-commit", "run", "--color=never", f"--files={args.output_markdown}"],  # noqa: S607,RUF100
            check=False,
        )


if __name__ == "__main__":
    main()
