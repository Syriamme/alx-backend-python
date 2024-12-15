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

    with patch.object(
        GithubOrgClient,
        "org",
        new_callable=PropertyMock
    )as n:
        n.return_value = {"repos_url": "89"}
        cl = GithubOrgClient("google")

        res = cl._public_repos_url

        self.assertEqual(res, n.return_value("repos_url"))
        n.assert_called_once()


@patch('client.get_json',
       return_value=[{'name': 'Repo1'}, {'name': 'Repo2'}, {'name': 'Repo3'}])
def test_public_repos(self, mock_get_json):
    """
    Test the 'public_repos' method in GithubOrgClient.
    """
    with patch.object(
        GithubOrgClient,
        '_public_repos_url',
        new_callable=PropertyMock,
        return_value="https://api.github.com/"
    ) as mock_repos_url:
        client = GithubOrgClient('holberton')
        repos_list = client.public_repos()
        for repo in ['Repo1', 'Repo2', 'Repo3']:
            self.assertIn(repo, repos_list)
        mock_get_json.assert_called_once()
        mock_repos_url.assert_called_once()
