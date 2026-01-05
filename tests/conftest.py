"""Pytest configuration and fixtures for SonarQube SDK tests.

This module provides common fixtures and configuration for all tests.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator
import respx

from sonarqube import SonarQubeClient
from sonarqube.auth import BasicAuth, TokenAuth
from sonarqube.http import HTTPClient


@pytest.fixture
def base_url() -> str:
    """Provide test base URL."""
    return "https://sonarqube.example.com"


@pytest.fixture
def token() -> str:
    """Provide test token."""
    return "test-token-12345"


@pytest.fixture
def token_auth(token: str) -> TokenAuth:
    """Provide token authentication."""
    return TokenAuth(token=token)


@pytest.fixture
def basic_auth() -> BasicAuth:
    """Provide basic authentication."""
    return BasicAuth(username="admin", password="admin")


@pytest.fixture
def http_client(
    base_url: str, token_auth: TokenAuth
) -> Generator[HTTPClient, None, None]:
    """Provide configured HTTP client."""
    client = HTTPClient(base_url=base_url, auth=token_auth)
    yield client
    client.close()


@pytest.fixture
def sonarqube_client(
    base_url: str, token: str
) -> Generator[SonarQubeClient, None, None]:
    """Provide configured SonarQube client."""
    client = SonarQubeClient(base_url=base_url, token=token)
    yield client
    client.close()


@pytest.fixture
def mock_api(base_url: str) -> Generator[respx.MockRouter, None, None]:
    """Provide mocked API for testing.

    Example:
        def test_projects_search(mock_api, sonarqube_client):
            mock_api.get("/api/projects/search").mock(
                return_value=Response(200, json={
                    "components": [],
                    "paging": {"pageIndex": 1, "pageSize": 100, "total": 0}
                })
            )

            response = sonarqube_client.projects.search()
            assert response.paging.total == 0
    """
    with respx.mock(base_url=base_url) as mock:
        yield mock


# Sample response data fixtures


@pytest.fixture
def sample_project_data() -> dict:
    """Provide sample project data."""
    return {
        "key": "my-project",
        "name": "My Project",
        "qualifier": "TRK",
        "visibility": "private",
        "lastAnalysisDate": "2025-01-01T12:00:00+0000",
    }


@pytest.fixture
def sample_paging_data() -> dict:
    """Provide sample paging data."""
    return {
        "pageIndex": 1,
        "pageSize": 100,
        "total": 1,
    }


@pytest.fixture
def sample_application_data() -> dict:
    """Provide sample application data."""
    return {
        "key": "my-app",
        "name": "My Application",
        "description": "A test application",
        "visibility": "private",
    }


@pytest.fixture
def sample_issue_data() -> dict:
    """Provide sample issue data."""
    return {
        "key": "AXoN-12345",
        "rule": "python:S1234",
        "severity": "MAJOR",
        "component": "my-project:src/main.py",
        "project": "my-project",
        "line": 42,
        "message": "Remove this unused variable",
        "status": "OPEN",
        "type": "CODE_SMELL",
    }


@pytest.fixture
def sample_rule_data() -> dict:
    """Provide sample rule data."""
    return {
        "key": "python:S1234",
        "repo": "python",
        "name": "Unused variables should be removed",
        "severity": "MAJOR",
        "lang": "py",
        "langName": "Python",
        "type": "CODE_SMELL",
    }
