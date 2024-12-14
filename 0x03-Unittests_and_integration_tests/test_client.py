#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch
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
    Test GithubOrgClient._public_repos_url property.
    Ensure it returns the expected repos_url from a mocked org response.
    """
    mocked_org_payload = {
        "repos_url": "https://api.github.com/orgs/google/repos"
    }

    # Patch the org property of GithubOrgClient to return the mocked payload
    with patch.object(
        GithubOrgClient,
        "org",
        new_callable=unittest.mock.PropertyMock,
        return_value=mocked_org_payload
    ):
        # Instantiate GithubOrgClient
        client = GithubOrgClient("google")

        # Test the _public_repos_url property
        result = client._public_repos_url

        # Assert that _public_repos_url returns
        # the repos_url from the mocked payload
        self.assertEqual(result, mocked_org_payload["repos_url"])
