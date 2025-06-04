from babel.messages import frontend as babel
from setuptools import setup

setup(
    packages=["jsonschema2md"],
    cmdclass={
        "compile_catalog": babel.compile_catalog,
        "extract_messages": babel.extract_messages,
        "init_catalog": babel.init_catalog,
        "update_catalog": babel.update_catalog,
    },
)
