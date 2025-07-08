# Localization

This folder holds all the locales for the program.

The locales are stored as `<lang>/LC_MESSAGES/messages.po`, where `lang` is a valid language identifier (ex: en_US).

## Create a new localization

1. To create a new locale (language), run the following commands after installing the project:

```sh
$ make extract # Creates the .pot file
$ make LANG=<lang> init # Generates the .po under <lang>/LC_MESSAGES/messages.po
```

2. Edit the .po file using a tool of your preference (for example, [POEdit](https://poedit.net/) or [Virtaal](https://virtaal.translatehouse.org/)).

3. After translating every string, compile it using the following command:

```sh
$ make compile # Generates <lang>/LC_MESSAGES/messages.mo
```

4. Test the program after compiling the translation:

```sh
$ jsonschema2md --locale <lang> schema.json out.md # You can use examples/ms2rescore.json as the schema.
```

5. Commit your changes:

```sh
$ git commit -m "Add <lang> translation."
```

## Editing an existing translation

1. Extract the messages with the following command:

```sh
$ make extract
```

2. Update the catalog:

```sh
$ make update
```

3. Edit the .po file using a tool of your preference (for example, [POEdit](https://poedit.net/) or [Virtaal](https://virtaal.translatehouse.org/)).

4. After editing, compile it using the following command:

```sh
$ make compile
```

5. Test the program after compiling the translation:

```sh
$ jsonschema2md --locale <lang> schema.json out.md # You can use examples/ms2rescore.json as the schema.
```

6. Commit your changes:

```sh
$ git commit -m "Update <lang> translation."
```

> **NOTE:** When editing the French (fr) or the Swiss French (fr_CH) locales, make sure the [tests](https://github.com/sbrunner/jsonschema2md/blob/master/tests/test_jsonschema2md.py) (TestParserFR class) reflect your changes. You can verify your changes with the command:
>
> ```sh
> $ pytest -vv -k "TestParserFR"
> ```
