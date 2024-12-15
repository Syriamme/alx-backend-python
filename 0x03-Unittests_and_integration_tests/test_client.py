#!/usr/bin/env python3
"""
Unit tests for GitHub Org Client
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit test for methods in the GithubOrgClient class
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org_nm, mock_json):
        """
        Testing the 'org' method.
        Args:
            org_nm (str): Name of org being tested
        """
        test_client = GithubOrgClient(org_nm)
        org_respo = test_client.org
        self.assertEqual(org_respo, mock_json.return_value)
        mock_json.assert_called_once()

    def test_public_repos_url(self):
        """
        est that the result of _public_repos_url
        is the expected one based on the mocked payload.
        """
        with patch.object(
             GithubOrgClient, 'org', new_callable=PropertyMock
             ) as mock_og:
            mock_og.return_value = {
                "repos_url": "https://api.github.com/users/google/repos"
            }
            client = GithubOrgClient('google')

            repos_url = client._public_repos_url

            result = mock_og.return_value['repos_url']

            self.assertEqual(repos_url, result)
            mock_og.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """
        Testing that the list of repos is
        what you expect from the chosen payload.
        Testing that the mocked property and
        the mocked get_json was called once.
        """
        mock_json.return_value = [
            {'name': 'Repos1'},
            {'name': 'Repos2'},
            {'name': 'Repos3'}
        ]
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/users/google/repos"
        ) as mock_repo_url:
            client = GithubOrgClient('google')

            repo_list = client.public_repos()

            self.assertCountEqual(repo_list, ['Repos1', 'Repos2', 'Repos3'])

            mock_json.assert_called_once()
            mock_repo_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, key, result):
        """
        Testing 'has_license' method
        with the expected returned value.

        Args:
            repo(dict): Repo data with the license information

            key (str): The license key being checked

            result (bool): Expected boolean value checking license
        """
        test_client = GithubOrgClient('google')
        with_license = test_client.has_license(repo, key)
        self.assertEqual(with_license, result)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            TEST_PAYLOAD[0]["org_payload"],
            TEST_PAYLOAD[0]["repos_payload"],
            TEST_PAYLOAD[0]["expected_repos"],
            TEST_PAYLOAD[0]["apache2_repos"],
        )
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.public_repos method.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method to mock requests.get and provide payloads.
        """
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return {}

        cls.get_patcher = patch("requests.get", side_effect=lambda url: MockResponse(side_effect(url)))
        cls.get_patcher.start()

        cls.client = GithubOrgClient("google")

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method to stop the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos method without filtering by license.
        """
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos method with filtering by a specific license.
        """
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"), self.apache2_repos
        )


class MockResponse:
    """
    Mock response for requests.get.
    """

    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data
