"""Tests for authentication handlers."""

from __future__ import annotations

import base64

import pytest

from sonarqube.auth import BasicAuth, TokenAuth, create_auth


class TestTokenAuth:
    """Tests for TokenAuth."""

    def test_init(self) -> None:
        """Test TokenAuth initialization."""
        auth = TokenAuth(token="my-token")
        assert auth.token == "my-token"

    def test_init_empty_token_raises(self) -> None:
        """Test that empty token raises ValueError."""
        with pytest.raises(ValueError, match="Token cannot be empty"):
            TokenAuth(token="")

    def test_get_auth_headers(self) -> None:
        """Test get_auth_headers returns correct headers."""
        auth = TokenAuth(token="my-token")
        headers = auth.get_auth_headers()

        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

        # Decode and verify
        encoded = headers["Authorization"].replace("Basic ", "")
        decoded = base64.b64decode(encoded).decode()
        assert decoded == "my-token:"


class TestBasicAuth:
    """Tests for BasicAuth."""

    def test_init(self) -> None:
        """Test BasicAuth initialization."""
        auth = BasicAuth(username="admin", password="secret")
        assert auth.username == "admin"
        assert auth.password == "secret"

    def test_init_empty_username_raises(self) -> None:
        """Test that empty username raises ValueError."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            BasicAuth(username="", password="secret")

    def test_get_auth_headers(self) -> None:
        """Test get_auth_headers returns correct headers."""
        auth = BasicAuth(username="admin", password="secret")
        headers = auth.get_auth_headers()

        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

        # Decode and verify
        encoded = headers["Authorization"].replace("Basic ", "")
        decoded = base64.b64decode(encoded).decode()
        assert decoded == "admin:secret"


class TestCreateAuth:
    """Tests for create_auth factory function."""

    def test_create_auth_with_token(self) -> None:
        """Test create_auth with token returns TokenAuth."""
        auth = create_auth(token="my-token")
        assert isinstance(auth, TokenAuth)

    def test_create_auth_with_credentials(self) -> None:
        """Test create_auth with credentials returns BasicAuth."""
        auth = create_auth(username="admin", password="secret")
        assert isinstance(auth, BasicAuth)

    def test_create_auth_token_takes_priority(self) -> None:
        """Test that token takes priority over credentials."""
        auth = create_auth(
            token="my-token",
            username="admin",
            password="secret",
        )
        assert isinstance(auth, TokenAuth)

    def test_create_auth_no_credentials_returns_none(self) -> None:
        """Test create_auth with no credentials returns None."""
        auth = create_auth()
        assert auth is None

    def test_create_auth_username_without_password_raises(self) -> None:
        """Test that username without password raises ValueError."""
        with pytest.raises(ValueError, match="Password is required"):
            create_auth(username="admin")
