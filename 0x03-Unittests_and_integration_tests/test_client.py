#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
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
def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        Tests the `public_repos` method.
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()