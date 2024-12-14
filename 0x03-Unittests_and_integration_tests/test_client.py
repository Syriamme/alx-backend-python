import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient 


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_response, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        
        Args:
            org_name (str): The name of the organization.
            mock_response (dict): The mocked response data.
            mock_get_json (Mock): The patched `get_json` method.
        """
        # Arrange: Set up the mock to return the expected response
        mock_get_json.return_value = mock_response

        # Act: Create a GithubOrgClient instance and call the `org` method
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: Verify that the `get_json` method was called with the correct argument
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, mock_response)
