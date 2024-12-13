#!/usr/bin/env python3
"""
Testing the access_nested_map function.
"""

import unittest
from parameterized import parameterized
from typing import Dict, Tuple, Union
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
    def test_access_nested_map(
        self,
        map_test,
        path,
        value,
    ):
        """
        Test the function returns the expected result.

        Args:
            map_test (dict): Dictionary to test.
            path (tuple): Key sequence.
            expected_value (Any): xpected result.
        """
        self.assertEqual(access_nested_map(map_test, path), value)
