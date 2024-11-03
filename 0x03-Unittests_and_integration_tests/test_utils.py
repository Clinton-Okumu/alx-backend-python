#!/usr/bin/env python3
"""
test_utils.py

This module contains unit tests for the functions in utils.py.
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """Test access_nested_map with various nested maps and paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence
    ) -> None:
        """Test that access_nested_map raises KeyError for invalid inputs.

        Args:
            nested_map: The nested dictionary to test with
            path: The sequence of keys that should trigger a KeyError
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], path[-1])


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self) -> None:
        """Test memoization of a method.

        Tests that when calling a_property twice, the correct result
        is returned but a_method is only called once.
        """
        class TestClass:
            """Test class for memoization."""

            def a_method(self):
                """Method to be memoized."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that returns a_method result."""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            first_call = test_obj.a_property
            second_call = test_obj.a_property
            mock_method.assert_called_once()
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)


if __name__ == "__main__":
    unittest.main()
