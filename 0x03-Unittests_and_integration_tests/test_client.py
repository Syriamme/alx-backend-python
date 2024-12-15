#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest 
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from urllib import response
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing the GithubOrgClient case
    """

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch(
        "client.get_json",
        return_value={"payload": True}
    )
    def test_org(self, org, mocked_org):
        """
        Testing if GithubOrgClient.org will return correct value

        get_json will be called once with the correct arg.
        Args:
            org(str): name of the organization
        """
        org_client = GithubOrgClient(org)

        response = org_client.org

        self.assertEqual(response, mocked_org.return_value)
        mocked_org.assert_called_once()


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
    Testing that the list of repos is what you expect from the chosen payload.
    Testing that the mocked property and the mocked get_json was called once.
    """
    mocked_payload = [
        {"name": "repo1", "license": {"key": "mit"}},
        {"name": "repo2", "license": {"key": "apache-2.0"}},
        {"name": "repo3", "license": {"key": "mit"}},
    ]
    mock_get_json.return_value = mocked_payload

    with patch.object(
        GithubOrgClient,
        "_public_repos_url",
        new_callable=unittest.mock.PropertyMock,
        return_value="https://api.github.com/orgs/google/repos"
    ) as mocked_repos_url:
        client = GithubOrgClient("google")

        result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2", "repo3"])

        mocked_repos_url.assert_called_once()

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )
