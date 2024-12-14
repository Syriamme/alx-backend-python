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
@patch("client.GithubOrgClient._public_repos_url",
       new_callable=unittest.mock.PropertyMock)
def test_public_repos(self, mock_public_repos_url, mock_get_json):
    mock_get_json.return_value = [
        {"name": "repo1"},
        {"name": "repo2"}
    ]
    mock_public_repos_url.return_value = (
        "https://api.github.com/orgs/test_org/repos"
    )
    client = GithubOrgClient("test_org")
    result = client.public_repos()
    self.assertEqual(result, ["repo1", "repo2"])
    mock_public_repos_url.assert_called_once()
    mock_get_json.assert_called_once_with(
        "https://api.github.com/orgs/test_org/repos"
    )
