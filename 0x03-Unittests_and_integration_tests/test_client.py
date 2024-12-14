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
def test_public_repos(mock_get_json):

    # Short test payload for Google repos
    test_payload_google = {
        'repos_url': "https://api.github.com/users/google/repos",
        'repos': [
            {"name": "google-api", "private": False},
            {"name": "google-cloud", "private": False}
        ]
    }

    # Mock the `get_json` method to return Google's repos payload
    mock_get_json.return_value = test_payload_google["repos"]

    # Mock the `_public_repos_url` property
    with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
        mock_public_repos_url.return_value = test_payload_google["repos_url"]

        # Create the GithubOrgClient instance for Google
        client_google = GithubOrgClient("google")

        # Call the `public_repos` method and assert the expected result
        assert client_google.public_repos() == ["google-api", "google-cloud"]

        # Ensure the mocked property and get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(test_payload_google["repos_url"])

    # Short test payload for Microsoft repos
    test_payload_microsoft = {
        'repos_url': "https://api.github.com/users/microsoft/repos",
        'repos': [
            {"name": "azure-sdk", "private": False},
            {"name": "microsoft-auth", "private": False}
        ]
    }

    # Mock the `get_json` method to return Microsoft's repos payload
    mock_get_json.return_value = test_payload_microsoft["repos"]

    # Mock the `_public_repos_url` property for Microsoft
    with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
        mock_public_repos_url.return_value = test_payload_microsoft["repos_url"]

        # Create the GithubOrgClient instance for Microsoft
        client_microsoft = GithubOrgClient("microsoft")

        # Call the `public_repos` method and assert the expected result
        assert client_microsoft.public_repos() == ["azure-sdk", "microsoft-auth"]

        # Ensure the mocked property and get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(test_payload_microsoft["repos_url"])