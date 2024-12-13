#!/usr/bin/env python3
"""
Testing the access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
import unittest
from unittest.mock import patch, Mock
from typing import Dict


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
            expected_value (Any): xpected result.
        """
        self.assertEqual(access_nested_map(map_test, path), value)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map,
            path,
            exception,
    ):
        """
        Tests `access_nested_map`'s exception raising.
        """
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test case class for ensuring that get_json
    function returns the expected result.
    The test class has a special focus
    on mocking external HTTP calls.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Mocked HTTP responses to test the function.
        This will return a mock object
        with a json method that returns test_payload
        Args:
            test_url(str): The url to be used.
            test_payload: The expected Json payload
            mock_get: Mocking the requests.get method.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)
        mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """
    Test case class for memoization behavior
    """
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                """
                Method that is being memoized
                """
                return 42

            @memoize
            def a_property(self):
                """
                Property calling a_method
                """
                return self.a_method()

        object = TestClass()

        with patch.object(object, 'a_method', return_value=42) as mock_method:
            res_1 = object.a_property
            res_2 = object.a_property

            self.assertEqual(res_1, 42)
            self.assertEqual(res_2, 42)

            mock_method.assert_called_once()
