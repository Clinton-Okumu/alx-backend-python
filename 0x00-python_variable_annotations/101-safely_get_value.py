#!/usr/bin/env python3
"""Contains a function with complex type annotations for safely
retrieving a value from a dictionary-like object."""
from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')

def safely_get_value(dct: Mapping, key: Any, default: Union[T, None] = None) -> Union[Any, T]:
    """Safely retrieves a value from a dictionary-like object.

    Args:
        dct: A dictionary-like object (Mapping).
        key: The key to look up in the dictionary.
        default: The default value to return if the key is not found.

    Returns:
        The value associated with the key if found, otherwise the default value.
    """
    if key in dct:
        return dct[key]
    else:
        return default
