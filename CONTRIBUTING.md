# Contributing

This document briefly describes how to contribute to
[jsonschema2md](https://github.com/ralfg/jsonschema2md).

## Before you begin

If you have an idea for a feature, use case to add or an approach for a bugfix,
you are welcome to communicate it with the community by creating an issue in
[GitHub issues](https://github.com/ralfg/jsonschema2md/issues).

## How to contribute

- Fork [jsonschema2md](https://github.com/ralfg/jsonschema2md) on GitHub to
  make your changes.
- Commit and push your changes to your
  [fork](https://help.github.com/articles/pushing-to-a-remote/).
- Open a
  [pull request](https://help.github.com/articles/creating-a-pull-request/)
  with these changes. You pull request message ideally should include:
  - A description of why the changes should be made.
  - A description of the implementation of the changes.
  - A description of how to test the changes.
- The pull request should pass all the continuous integration tests which are
  automatically run by
  [GitHub Actions](https://github.com/ralfg/jsonschema2md/actions).

## Development setup

1. Setup Python 3 and [Poetry](https://python-poetry.org/docs/)
2. Clone the [jsonschema2md repository](https://github.com/ralfg/jsonschema2md) and
   run `poetry install` to setup the development environment.

## Development workflow

- When a new version is ready to be published:
  1. Change the `__version__` in `pyproject.toml` following
     [semantic versioning](https://semver.org/).
  2. Update the documentation (`README.md`), if required.
  3. Update the changelog (if not already done) in `CHANGELOG.md` according to
     [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
  4. Commit all final changes to the `master` branch.
  5. On `master`, set a new tag with the version number, e.g. `git tag v0.1.5`.
  6. Push to GitHub, with the tag: `git push; git push --tags`.

- When a new tag is pushed to (or made on) GitHub that matches `v*`, the
  following GitHub Actions are triggered:

      1. The Python package is build and published to PyPI.
      2. Using the [Git Release](https://github.com/marketplace/actions/git-release)
      action, a new GitHub release is made with the changes that are listed in
      `CHANGELOG.md`.
