#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing the GithubOrgClient case
    """

    @parameterized.expand([
        ("google", {"login": "value"}),
        ("abc", {"login": "value"}),
    ])
    @patch(
        "client.get_json",
    )
    def test_org(self, org, response, mocked_get_json):
        """
        Testing if GithubOrgClient.org will return correct value

        get_json will be called once with the correct arg.
        """

        mocked_get_json.return_value = response
        client = GithubOrgClient(org)
        result = client.org

        mocked_get_json.assert_called_once_with
        (f"https://api.github.com/orgs/{org}")

        self.assertEqual(result, response)


def test_public_repos_url(self):
    """
    Testing that the result of _public_repos_url
    is the expected one based on the mocked payload.
    """
    mocked_payload = {
        "repos_url": "https://api.github.com/orgs/google/repos"
    }

    with patch.object(
        GithubOrgClient,
        "org",
        new_callable=unittest.mock.PropertyMock,
        return_value=mocked_payload
    ):
        cl = GithubOrgClient("google")

        res = cl._public_repos_url

        self.assertEqual(res, mocked_payload["repos_url"])


@patch("client.get_json")
def test_public_repos(self, mock_get_json):
    """Test the public_repos method of GithubOrgClient."""

    # Define the test payload
    test_payload = {
        "repos_url": "https://api.github.com/orgs/google/repos",
        "repos": [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
    }

    # Set the mock response for get_json to return the 'repos' part of the payload
    mock_get_json.return_value = test_payload["repos"]

    # Mock the _public_repos_url property to return the mock URL
    with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
        mock_public_repos_url.return_value = test_payload["repos_url"]

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("google")

        # Test without any license filter
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2", "repo3"])  # All repositories should be returned

        # Test with a specific license filter (e.g., "mit")
        result_with_license = client.public_repos(license="mit")
        self.assertEqual(result_with_license, ["repo1", "repo3"])  # Only "repo1" and "repo3" should be returned

        # Verify that the _public_repos_url property was accessed once
        mock_public_repos_url.assert_called_once()

        # Verify that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(test_payload["repos_url"])
