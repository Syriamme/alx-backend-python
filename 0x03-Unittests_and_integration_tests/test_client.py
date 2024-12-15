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
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_og:
            mock_og.return_value = {"repos_url": "https://api.github.com/users/google/repos"}

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
            return_value="https://api.github.com/") as mock_repo_url:

            client = GithubOrgClient('google')

            repo_list = client.public_repos()
            
            self.assertCountEqual(repo_list, ['Repos1', 'Repos2', 'Repos3'])

            mock_json.assert_called_once()
            mock_repo_url.assert_called_once()

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
