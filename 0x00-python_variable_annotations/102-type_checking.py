#!/usr/bin/env python3
"""Contains a function with type annotations for creating a zoomed array,
along with example usage that passes mypy type checking."""
from typing import List, Tuple

def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> List[int]:
    """Creates a new list with each element of the input tuple repeated based on the factor.

    Args:
        lst: A tuple of integers to be zoomed.
        factor: The number of times each element should be repeated. Defaults to 2.

    Returns:
        A list with each element from the input tuple repeated 'factor' times.
    """
    zoomed_in: List[int] = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in
