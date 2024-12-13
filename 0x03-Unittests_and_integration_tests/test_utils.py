#!/usr/bin/env python3
"""
Testing the access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    access_nested_map function test case.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, map_test, path, value):
        """
        Test the function returns the expected result.

        Args:
            map_test (dict): Dictionary to test.
            path (tuple): Key sequence.
            expected_value (Any): expected result.
        """
        self.assertEqual(access_nested_map(map_test, path), value)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, map_test, path, exception):
        """
        Test the function raises an exception.

        Args:
            map_test (dict): Dictionary to test.
            path (tuple): Key sequence.
            exception (Any): expected to be raised.
        """
        with self.assertRaises(exception):
            (access_nested_map(map_test, path))
