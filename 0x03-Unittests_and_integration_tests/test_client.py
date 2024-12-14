#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class"""

    @parameterized.expand([
        ("google", {"key": "value"}),  # Example 1: org_name = "google"
        ("abc", {"key": "another_value"}),  # Example 2: org_name = "abc"
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and get_json is called once with the correct argument.
        """
        # Mock the response of get_json
        mock_get_json.return_value = expected_response

        # Instantiate GithubOrgClient with the org_name
        client = GithubOrgClient(org_name)

        # Access the org property (no parentheses)
        result = client.org

        # Assert that the mocked get_json was called once with the correct URL
        mock_get_json.assert_called_once_with
        (f"https://api.github.com/orgs/{org_name}")

        # Assert that the org method returns the mocked response
        self.assertEqual(result, expected_response)
