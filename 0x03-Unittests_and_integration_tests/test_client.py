#!/usr/bin/env python3
"""
Module for testing the client GithubOrgClient.
This module contains both unit tests and integration tests to verify
the functionality of the GithubOrgClient class and its methods.
Tests include mocking of external requests, property tests, and
parameterized testing for various scenarios.
"""

import unittest
from typing import Dict, List
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
import requests


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for GithubOrgClient class.
    This class contains unit tests for all methods in GithubOrgClient,
    utilizing mocking to avoid actual API calls.
    """
    @parameterized.expand([
        "google",
        "abc",
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: PropertyMock) -> None:
        """
        Test the org method of GithubOrgClient.
        """
        test_client = GithubOrgClient(org_name)
        test_client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self) -> None:
        """
        Test the _public_repos_url property of GithubOrgClient.
        This test mocks the org property to return a known payload
        and verifies the proper URL is generated.
        """
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            test_client = GithubOrgClient("test")
            url = test_client._public_repos_url
            mock_org.assert_called_once()
            self.assertEqual(url, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: PropertyMock) -> None:
        """
        Test the public_repos method of GithubOrgClient.
        Args:
            mock_get_json: Mocked get_json function
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ) as mock_pub:
            test_client = GithubOrgClient("test")
            repos = test_client.public_repos()
            mock_pub.assert_called_once()
            mock_get_json.assert_called_once()
            self.assertEqual(repos, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict,
        license_key: str,
        expected: bool
    ) -> None:
        """
        Test the has_license static method of GithubOrgClient.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test suite for GithubOrgClient class.
    This class implements integration tests using fixtures to test
    the actual integration of various GithubOrgClient methods.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up class fixtures before running tests.
        This method sets up the patches for the requests.get method
        that will be used across all tests.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> unittest.mock.Mock:
            """
            Define the side effect for the mock get request.
            """
            mock_response = unittest.mock.Mock()
            if url.endswith('/orgs/test'):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith('/repos'):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down class fixtures after running tests.
        This method stops all patches that were started in setUpClass.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Integration test for the public_repos method.
        Tests the public_repos method with the fixture data.
        """
        test_client = GithubOrgClient("test")
        self.assertEqual(test_client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Integration test for the public_repos method with license filter.
        Tests the public_repos method with the apache-2.0 license filter.
        """
        test_client = GithubOrgClient("test")
        self.assertEqual(
            test_client.public_repos(license="apache-2.0"),
            self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
