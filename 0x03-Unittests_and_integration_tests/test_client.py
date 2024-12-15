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
    def test_org(self, org_name, mock_get_json):
        """
        Test the 'org' method in GithubOrgClient.
        Args:
            org_name (str): Name of the organization to test
        """
        client = GithubOrgClient(org_name)
        org_response = client.org
        self.assertEqual(org_response, mock_get_json.return_value)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """
        Test the '_public_repos_url' property of GithubOrgClient.
        """
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/holberton/repos"}
            client = GithubOrgClient('holberton')
            repos_url = client._public_repos_url
            self.assertEqual(repos_url, mock_org.return_value['repos_url'])
            mock_org.assert_called_once()

    @patch('client.get_json', return_value=[{'name': 'Repo1'}, {'name': 'Repo2'}, {'name': 'Repo3'}])
    def test_public_repos(self, mock_get_json):
        """
        Test the 'public_repos' method in GithubOrgClient.
        """
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock, return_value="https://api.github.com/") as mock_repos_url:
            client = GithubOrgClient('holberton')
            repos_list = client.public_repos()
            for repo in ['Repo1', 'Repo2', 'Repo3']:
                self.assertIn(repo, repos_list)
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo_data, license_key, expected_result):
        """
        Test the 'has_license' method in GithubOrgClient.
        
        Args:
            repo_data (dict): The repository data containing license info
            license_key (str): The license key to check for
            expected_result (bool): Expected boolean result for the license check
        """
        client = GithubOrgClient('holberton')
        has_license = client.has_license(repo_data, license_key)
        self.assertEqual(has_license, expected_result)


def mock_requests_get(*args, **kwargs):
    """
    Mocked requests.get function to simulate API responses.
    
    Args:
        *args: Positional arguments (URL)
        **kwargs: Keyword arguments (params, headers)
    """
    class MockResponse:
        """
        A mock class to simulate the behavior of a real HTTP response.
        """
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == "https://api.github.com/orgs/google":
        return MockResponse(TEST_PAYLOAD[0][0])
    if args[0] == TEST_PAYLOAD[0][0]["repos_url"]:
        return MockResponse(TEST_PAYLOAD[0][1])


@parameterized_class(
    ('org_data', 'repos_data', 'expected_repos', 'apache2_repos'),
    [(TEST_PAYLOAD[0][0], TEST_PAYLOAD[0][1], TEST_PAYLOAD[0][2], TEST_PAYLOAD[0][3])]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the 'public_repos' method in GithubOrgClient.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment for the class.
        """
        cls.patcher = patch('utils.requests.get', side_effect=mock_requests_get)
        cls.patcher.start()
        cls.client = GithubOrgClient('google')

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after tests and stop patching.
        """
        cls.patcher.stop()

    def test_public_repos(self):
        """
        Test the 'public_repos' method without specifying a license.
        """
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the 'public_repos' method with the license filter.
        """
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )