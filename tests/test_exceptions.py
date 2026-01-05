"""Tests for exceptions."""

from __future__ import annotations

from sonarqube.exceptions import (
    SonarQubeAPIError,
    SonarQubeAuthenticationError,
    SonarQubeConnectionError,
    SonarQubeError,
    SonarQubeNotFoundError,
    SonarQubePermissionError,
    SonarQubeValidationError,
)


class TestSonarQubeError:
    """Tests for SonarQubeError base exception."""

    def test_init(self) -> None:
        """Test SonarQubeError initialization."""
        error = SonarQubeError(message="Test error")
        assert error.message == "Test error"
        assert error.details is None

    def test_init_with_details(self) -> None:
        """Test SonarQubeError with details."""
        error = SonarQubeError(message="Test error", details={"key": "value"})
        assert error.message == "Test error"
        assert error.details == {"key": "value"}

    def test_str(self) -> None:
        """Test SonarQubeError string representation."""
        error = SonarQubeError(message="Test error")
        assert str(error) == "Test error"

    def test_str_with_details(self) -> None:
        """Test SonarQubeError string with details."""
        error = SonarQubeError(message="Test error", details="extra info")
        assert str(error) == "Test error: extra info"


class TestSonarQubeAPIError:
    """Tests for SonarQubeAPIError."""

    def test_init(self) -> None:
        """Test SonarQubeAPIError initialization."""
        error = SonarQubeAPIError(message="API error", status_code=500)
        assert error.message == "API error"
        assert error.status_code == 500
        assert error.errors == []

    def test_init_with_errors(self) -> None:
        """Test SonarQubeAPIError with error objects."""
        errors = [{"msg": "Error 1"}, {"msg": "Error 2"}]
        error = SonarQubeAPIError(
            message="API error",
            status_code=400,
            errors=errors,
        )
        assert error.errors == errors

    def test_str(self) -> None:
        """Test SonarQubeAPIError string representation."""
        error = SonarQubeAPIError(message="API error", status_code=500)
        assert str(error) == "[500] API error"

    def test_str_with_errors(self) -> None:
        """Test SonarQubeAPIError string with error messages."""
        errors = [{"msg": "Error 1"}, {"msg": "Error 2"}]
        error = SonarQubeAPIError(
            message="API error",
            status_code=400,
            errors=errors,
        )
        assert "[400]" in str(error)
        assert "Error 1" in str(error)
        assert "Error 2" in str(error)


class TestSpecificErrors:
    """Tests for specific error types."""

    def test_authentication_error(self) -> None:
        """Test SonarQubeAuthenticationError."""
        error = SonarQubeAuthenticationError()
        assert error.status_code == 401
        assert error.message == "Authentication failed"

    def test_permission_error(self) -> None:
        """Test SonarQubePermissionError."""
        error = SonarQubePermissionError()
        assert error.status_code == 403
        assert error.message == "Permission denied"

    def test_not_found_error(self) -> None:
        """Test SonarQubeNotFoundError."""
        error = SonarQubeNotFoundError()
        assert error.status_code == 404
        assert error.message == "Resource not found"

    def test_validation_error(self) -> None:
        """Test SonarQubeValidationError."""
        errors = [{"msg": "Invalid value"}]
        error = SonarQubeValidationError(errors=errors)
        assert error.status_code == 400
        assert error.errors == errors

    def test_connection_error(self) -> None:
        """Test SonarQubeConnectionError."""
        error = SonarQubeConnectionError()
        assert error.message == "Failed to connect to SonarQube"

    def test_exception_hierarchy(self) -> None:
        """Test that all exceptions inherit from SonarQubeError."""
        assert issubclass(SonarQubeAPIError, SonarQubeError)
        assert issubclass(SonarQubeAuthenticationError, SonarQubeAPIError)
        assert issubclass(SonarQubePermissionError, SonarQubeAPIError)
        assert issubclass(SonarQubeNotFoundError, SonarQubeAPIError)
        assert issubclass(SonarQubeValidationError, SonarQubeAPIError)
        assert issubclass(SonarQubeConnectionError, SonarQubeError)
