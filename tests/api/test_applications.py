"""Tests for Applications API."""

from __future__ import annotations

import respx
from httpx import Response

from sonarqube import SonarQubeClient
from sonarqube.models.applications import (
    ApplicationCreateResponse,
    ApplicationSearchResponse,
    ApplicationShowResponse,
)


class TestApplicationsAPI:
    """Tests for ApplicationsAPI."""

    @respx.mock
    def test_create(
        self,
        sonarqube_client: SonarQubeClient,
        sample_application_data: dict,
    ) -> None:
        """Test application creation."""
        respx.post("/api/applications/create").mock(
            return_value=Response(
                200,
                json={"application": sample_application_data},
            )
        )

        response = sonarqube_client.applications.create(
            name="My Application",
            key="my-app",
            visibility="private",
        )

        assert isinstance(response, ApplicationCreateResponse)
        assert response.application.key == "my-app"
        assert response.application.name == "My Application"

    @respx.mock
    def test_delete(self, sonarqube_client: SonarQubeClient) -> None:
        """Test application deletion."""
        respx.post("/api/applications/delete").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.delete(application="my-app")

    @respx.mock
    def test_show(
        self,
        sonarqube_client: SonarQubeClient,
        sample_application_data: dict,
    ) -> None:
        """Test showing application."""
        respx.get("/api/applications/show").mock(
            return_value=Response(
                200,
                json={"application": sample_application_data},
            )
        )

        response = sonarqube_client.applications.show(application="my-app")

        assert isinstance(response, ApplicationShowResponse)
        assert response.application.key == "my-app"

    @respx.mock
    def test_search(
        self,
        sonarqube_client: SonarQubeClient,
        sample_application_data: dict,
        sample_paging_data: dict,
    ) -> None:
        """Test searching applications."""
        respx.get("/api/applications/search").mock(
            return_value=Response(
                200,
                json={
                    "paging": sample_paging_data,
                    "applications": [sample_application_data],
                },
            )
        )

        response = sonarqube_client.applications.search(q="my-app")

        assert isinstance(response, ApplicationSearchResponse)
        assert len(response.applications) == 1
        assert response.applications[0].key == "my-app"

    @respx.mock
    def test_add_project(self, sonarqube_client: SonarQubeClient) -> None:
        """Test adding project to application."""
        respx.post("/api/applications/add_project").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.add_project(
            application="my-app",
            project="my-project",
        )

    @respx.mock
    def test_remove_project(self, sonarqube_client: SonarQubeClient) -> None:
        """Test removing project from application."""
        respx.post("/api/applications/remove_project").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.remove_project(
            application="my-app",
            project="my-project",
        )

    @respx.mock
    def test_update(self, sonarqube_client: SonarQubeClient) -> None:
        """Test updating application."""
        respx.post("/api/applications/update").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.update(
            application="my-app",
            name="Updated Name",
            description="Updated description",
        )

    @respx.mock
    def test_set_tags(self, sonarqube_client: SonarQubeClient) -> None:
        """Test setting application tags."""
        respx.post("/api/applications/set_tags").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.set_tags(
            application="my-app",
            tags=["team-a", "production"],
        )

    @respx.mock
    def test_create_branch(self, sonarqube_client: SonarQubeClient) -> None:
        """Test creating application branch."""
        respx.post("/api/applications/create_branch").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.create_branch(
            application="my-app",
            branch="feature-x",
            project=["project1", "project2"],
        )

    @respx.mock
    def test_delete_branch(self, sonarqube_client: SonarQubeClient) -> None:
        """Test deleting application branch."""
        respx.post("/api/applications/delete_branch").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.applications.delete_branch(
            application="my-app",
            branch="feature-x",
        )
