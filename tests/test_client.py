"""Tests for SonarQubeClient."""

from __future__ import annotations

from sonarqube import SonarQubeClient
from sonarqube.api.applications import ApplicationsAPI
from sonarqube.api.components import ComponentsAPI
from sonarqube.api.hotspots import HotspotsAPI
from sonarqube.api.issues import IssuesAPI
from sonarqube.api.measures import MeasuresAPI
from sonarqube.api.projects import ProjectsAPI
from sonarqube.api.qualitygates import QualityGatesAPI
from sonarqube.api.qualityprofiles import QualityProfilesAPI
from sonarqube.api.rules import RulesAPI
from sonarqube.api.settings import SettingsAPI
from sonarqube.api.sources import SourcesAPI
from sonarqube.api.system import SystemAPI
from sonarqube.api.user_tokens import UserTokensAPI
from sonarqube.api.users import UsersAPI


class TestSonarQubeClientInit:
    """Tests for SonarQubeClient initialization."""

    def test_init_with_token(self, base_url: str, token: str) -> None:
        """Test client initialization with token authentication."""
        client = SonarQubeClient(base_url=base_url, token=token)
        assert client.base_url == base_url
        client.close()

    def test_init_with_basic_auth(self, base_url: str) -> None:
        """Test client initialization with basic authentication."""
        client = SonarQubeClient(
            base_url=base_url,
            username="admin",
            password="admin",
        )
        assert client.base_url == base_url
        client.close()

    def test_init_strips_trailing_slash(self, token: str) -> None:
        """Test that trailing slash is stripped from base URL."""
        client = SonarQubeClient(
            base_url="https://example.com/",
            token=token,
        )
        assert client.base_url == "https://example.com"
        client.close()

    def test_context_manager(self, base_url: str, token: str) -> None:
        """Test client as context manager."""
        with SonarQubeClient(base_url=base_url, token=token) as client:
            assert client.base_url == base_url


class TestSonarQubeClientAPIs:
    """Tests for SonarQubeClient API namespace properties."""

    def test_applications_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test applications property returns ApplicationsAPI."""
        assert isinstance(sonarqube_client.applications, ApplicationsAPI)

    def test_components_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test components property returns ComponentsAPI."""
        assert isinstance(sonarqube_client.components, ComponentsAPI)

    def test_hotspots_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test hotspots property returns HotspotsAPI."""
        assert isinstance(sonarqube_client.hotspots, HotspotsAPI)

    def test_issues_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test issues property returns IssuesAPI."""
        assert isinstance(sonarqube_client.issues, IssuesAPI)

    def test_measures_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test measures property returns MeasuresAPI."""
        assert isinstance(sonarqube_client.measures, MeasuresAPI)

    def test_projects_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test projects property returns ProjectsAPI."""
        assert isinstance(sonarqube_client.projects, ProjectsAPI)

    def test_qualitygates_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test qualitygates property returns QualityGatesAPI."""
        assert isinstance(sonarqube_client.qualitygates, QualityGatesAPI)

    def test_qualityprofiles_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test qualityprofiles property returns QualityProfilesAPI."""
        assert isinstance(sonarqube_client.qualityprofiles, QualityProfilesAPI)

    def test_rules_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test rules property returns RulesAPI."""
        assert isinstance(sonarqube_client.rules, RulesAPI)

    def test_settings_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test settings property returns SettingsAPI."""
        assert isinstance(sonarqube_client.settings, SettingsAPI)

    def test_sources_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test sources property returns SourcesAPI."""
        assert isinstance(sonarqube_client.sources, SourcesAPI)

    def test_system_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test system property returns SystemAPI."""
        assert isinstance(sonarqube_client.system, SystemAPI)

    def test_users_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test users property returns UsersAPI."""
        assert isinstance(sonarqube_client.users, UsersAPI)

    def test_user_tokens_property(self, sonarqube_client: SonarQubeClient) -> None:
        """Test user_tokens property returns UserTokensAPI."""
        assert isinstance(sonarqube_client.user_tokens, UserTokensAPI)

    def test_lazy_initialization(self, sonarqube_client: SonarQubeClient) -> None:
        """Test that API instances are lazily initialized."""
        # First access creates the instance
        projects1 = sonarqube_client.projects
        # Second access returns the same instance
        projects2 = sonarqube_client.projects
        assert projects1 is projects2
