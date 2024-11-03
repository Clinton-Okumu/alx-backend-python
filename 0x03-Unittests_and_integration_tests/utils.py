#!/usr/bin/env python3
"""
test_utils.py

This module contains unit tests for the functions in utils.py.
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """
        Test access_nested_map with various nested maps and paths.

        Parameters
        ----------
        nested_map : Mapping
            The nested dictionary to test with.
        path : Sequence
            The sequence of keys leading to the desired value.
        expected : Any
            The expected value at the given path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
        """
        Test access_nested_map raises KeyError for missing paths.

        Parameters
        ----------
        nested_map : Mapping
            The nested dictionary to test with.
        path : Sequence
            The sequence of keys leading to the missing value.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), str(path[-1]))


if __name__ == "__main__":
    unittest.main()
