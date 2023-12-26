import importlib.metadata
from typing import Union

__version__ = importlib.metadata.version("json-literal")

null = None
"""Definition of `null` value for pasting JSON data directly into python code and using it."""

true = True
"""Definition of `true` value for pasting JSON data directly into python code and using it."""

false = False
"""Definition of `false` value for pasting JSON data directly into python code and using it."""

Json = Union[None, bool, int, float, str, list["Json"], dict[str, "Json"]]

__all__ = (
    "null",
    "true",
    "false",
    "Json",
)
