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


@patch("client.get_json", return_value=[{'name': '.allstar'},
                                            {'name': '.github'},
                                            {'name': 'abpackage'}])
def test_public_repos(self, mock_repos):
    """
    Testing that the list of repos is what you expect from the chosen payload.
    Testing that the mocked property and the mocked get_json was called once.
    """

    with patch.object(
        GithubOrgClient,
        "_public_repos_url",
        new_callable=PropertyMock,
        return_value="https://api.github.com/users/google/repos"
    ) as m:
        test_client = GithubOrgClient("google")

        test_rep = test_client.public_repos()

        self.assertEqual(mock_repos.return_value, test_rep)

        mock_repos.assert_called_once()

        m.assert_called_once_with()
