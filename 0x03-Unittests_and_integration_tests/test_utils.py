import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function.
    """

    @parameterized.expand([
        ("simple_key", {"a": 1}, ("a",), 1),
        ("nested_key", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deeply_nested_key", {"a": {"b": 2}}, ("a", "b"), 2),
        ("missing_key", {"a": {"b": 2}}, ("a", "c"), KeyError),  # Add this test to check for missing keys
    ])
    def test_access_nested_map(self, _, nested_map, path, expected):
        """
        Test that access_nested_map returns
        the expected result for given inputs.

        Args:
            _: Unused, a placeholder for the test name.
            nested_map (dict): The dictionary to test.
            path (tuple): The sequence of keys to test.
            expected (Any): The expected result or exception.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            # If the expected result is an exception, check if it is raised
            with self.assertRaises(expected):
                access_nested_map(nested_map, path)
        else:
            # Otherwise, check if the actual result matches the expected
            self.assertEqual(access_nested_map(nested_map, path), expected)

