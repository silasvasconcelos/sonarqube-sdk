"""Tests for HTTP client."""

from __future__ import annotations

import pytest
import respx
from httpx import Response

from sonarqube.auth import TokenAuth
from sonarqube.exceptions import (
    SonarQubeAPIError,
    SonarQubeAuthenticationError,
    SonarQubeNotFoundError,
    SonarQubePermissionError,
    SonarQubeValidationError,
)
from sonarqube.http import HTTPClient


class TestHTTPClient:
    """Tests for HTTPClient."""

    def test_init(self, base_url: str, token_auth: TokenAuth) -> None:
        """Test HTTPClient initialization."""
        client = HTTPClient(base_url=base_url, auth=token_auth)
        assert client.base_url == base_url
        client.close()

    def test_init_strips_trailing_slash(self, token_auth: TokenAuth) -> None:
        """Test that trailing slash is stripped from base URL."""
        client = HTTPClient(
            base_url="https://example.com/",
            auth=token_auth,
        )
        assert client.base_url == "https://example.com"
        client.close()

    def test_context_manager(self, base_url: str, token_auth: TokenAuth) -> None:
        """Test HTTPClient as context manager."""
        with HTTPClient(base_url=base_url, auth=token_auth) as client:
            assert client.base_url == base_url


class TestHTTPClientRequests:
    """Tests for HTTPClient request methods."""

    @respx.mock
    def test_get(self, http_client: HTTPClient) -> None:
        """Test GET request."""
        respx.get("/api/test").mock(
            return_value=Response(200, json={"result": "success"})
        )

        response = http_client.get("/api/test")
        assert response == {"result": "success"}

    @respx.mock
    def test_post(self, http_client: HTTPClient) -> None:
        """Test POST request."""
        respx.post("/api/test").mock(
            return_value=Response(200, json={"result": "created"})
        )

        response = http_client.post("/api/test", data={"name": "test"})
        assert response == {"result": "created"}

    @respx.mock
    def test_get_with_params(self, http_client: HTTPClient) -> None:
        """Test GET request with query parameters."""
        respx.get("/api/test").mock(
            return_value=Response(200, json={"result": "success"})
        )

        response = http_client.get("/api/test", params={"q": "search"})
        assert response == {"result": "success"}

    @respx.mock
    def test_handles_204_no_content(self, http_client: HTTPClient) -> None:
        """Test handling of 204 No Content response."""
        respx.post("/api/test").mock(return_value=Response(204))

        response = http_client.post("/api/test")
        assert response == {}


class TestHTTPClientErrorHandling:
    """Tests for HTTPClient error handling."""

    @respx.mock
    def test_401_raises_authentication_error(self, http_client: HTTPClient) -> None:
        """Test that 401 response raises SonarQubeAuthenticationError."""
        respx.get("/api/test").mock(
            return_value=Response(
                401,
                json={"errors": [{"msg": "Invalid token"}]},
            )
        )

        with pytest.raises(SonarQubeAuthenticationError) as exc_info:
            http_client.get("/api/test")

        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value)

    @respx.mock
    def test_403_raises_permission_error(self, http_client: HTTPClient) -> None:
        """Test that 403 response raises SonarQubePermissionError."""
        respx.get("/api/test").mock(
            return_value=Response(
                403,
                json={"errors": [{"msg": "Permission denied"}]},
            )
        )

        with pytest.raises(SonarQubePermissionError) as exc_info:
            http_client.get("/api/test")

        assert exc_info.value.status_code == 403

    @respx.mock
    def test_404_raises_not_found_error(self, http_client: HTTPClient) -> None:
        """Test that 404 response raises SonarQubeNotFoundError."""
        respx.get("/api/test").mock(
            return_value=Response(
                404,
                json={"errors": [{"msg": "Not found"}]},
            )
        )

        with pytest.raises(SonarQubeNotFoundError) as exc_info:
            http_client.get("/api/test")

        assert exc_info.value.status_code == 404

    @respx.mock
    def test_400_raises_validation_error(self, http_client: HTTPClient) -> None:
        """Test that 400 response raises SonarQubeValidationError."""
        respx.post("/api/test").mock(
            return_value=Response(
                400,
                json={"errors": [{"msg": "Invalid parameter"}]},
            )
        )

        with pytest.raises(SonarQubeValidationError) as exc_info:
            http_client.post("/api/test")

        assert exc_info.value.status_code == 400
        assert len(exc_info.value.errors) == 1

    @respx.mock
    def test_500_raises_api_error(self, http_client: HTTPClient) -> None:
        """Test that 500 response raises SonarQubeAPIError."""
        respx.get("/api/test").mock(
            return_value=Response(
                500,
                json={"errors": [{"msg": "Internal error"}]},
            )
        )

        with pytest.raises(SonarQubeAPIError) as exc_info:
            http_client.get("/api/test")

        assert exc_info.value.status_code == 500
