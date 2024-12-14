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
    """
    Test GithubOrgClient.public_repos method.
    Ensure it returns the expected list of repository names.
    """
    # Mock payload to be returned by get_json
    mocked_repos_payload = [
        {"name": "repo1"},
        {"name": "repo2"},
    ]
    mock_get_json.return_value = mocked_repos_payload

    # Mock the _public_repos_url property
    with patch.object(
        GithubOrgClient,
        "_public_repos_url",
        new_callable=unittest.mock.PropertyMock,
        return_value="https://api.github.com/orgs/google/repos"
    ) as mock_repos_url:
        # Instantiate GithubOrgClient
        client = GithubOrgClient("google")

        # Call the public_repos method
        result = client.public_repos()

        # Assert the returned list matches the expected repo names
        self.assertEqual(result, ["repo1", "repo2"])

        # Assert the mocked property was called once
        mock_repos_url.assert_called_once()

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with
        ("https://api.github.com/orgs/google/repos")
