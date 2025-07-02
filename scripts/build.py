# ruff: noqa: INP001, D103
import logging
import sys
from pathlib import Path
from typing import Any

from babel.messages.frontend import CompileCatalog

log = logging.getLogger(__name__)


def initialize_options(compiler: CompileCatalog, **options: Any) -> None:
    compiler.initialize_options()  # type: ignore[no-untyped-call]

    for key, value in options.items():
        setattr(compiler, key, value)

    compiler.ensure_finalized()  # type: ignore[no-untyped-call]


def main() -> int:
    locales = Path("jsonschema2md/locales")
    languages = tuple(lang for lang in locales.iterdir() if lang.is_dir())

    res = 0

    for language in languages:
        compiler = CompileCatalog()  # type: ignore[no-untyped-call]

        initialize_options(
            compiler,
            directory=str(locales),
            locale=language.name,
            use_fuzzy=True,
            log=log,
        )

        res = compiler.run()  # type: ignore[no-untyped-call]

    if not languages:
        log.info("No languages found.")

    return res


if __name__ == "__main__":
    handler = logging.StreamHandler()
    log.addHandler(handler)
    log.setLevel(logging.INFO)

    sys.exit(main())
