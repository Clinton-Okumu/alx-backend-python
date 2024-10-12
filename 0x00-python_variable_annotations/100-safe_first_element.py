#!/usr/bin/env python3
"""Contains a function with duck-typed annotations for safely
retrieving the first element of a sequence."""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Returns the first element of a sequence if it exists, else None.

    Args:
        lst: A sequence of elements of any type.

    Returns:
        The first element of the sequence if it exists, otherwise None.
    """
    if lst:
        return lst[0]
    else:
        return None
