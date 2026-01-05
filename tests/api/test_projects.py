"""Tests for Projects API."""

from __future__ import annotations

import respx
from httpx import Response

from sonarqube import SonarQubeClient
from sonarqube.models.projects import ProjectSearchResponse


class TestProjectsAPI:
    """Tests for ProjectsAPI."""

    @respx.mock
    def test_search(
        self,
        sonarqube_client: SonarQubeClient,
        sample_project_data: dict,
        sample_paging_data: dict,
    ) -> None:
        """Test projects search."""
        respx.get("/api/projects/search").mock(
            return_value=Response(
                200,
                json={
                    "paging": sample_paging_data,
                    "components": [sample_project_data],
                },
            )
        )

        response = sonarqube_client.projects.search(q="my-project")

        assert isinstance(response, ProjectSearchResponse)
        assert response.paging.total == 1
        assert len(response.components) == 1
        assert response.components[0].key == "my-project"

    @respx.mock
    def test_search_with_pagination(
        self,
        sonarqube_client: SonarQubeClient,
        sample_paging_data: dict,
    ) -> None:
        """Test projects search with pagination parameters."""
        respx.get("/api/projects/search").mock(
            return_value=Response(
                200,
                json={
                    "paging": sample_paging_data,
                    "components": [],
                },
            )
        )

        response = sonarqube_client.projects.search(p=2, ps=50)

        assert isinstance(response, ProjectSearchResponse)

    @respx.mock
    def test_create(
        self,
        sonarqube_client: SonarQubeClient,
        sample_project_data: dict,
    ) -> None:
        """Test project creation."""
        respx.post("/api/projects/create").mock(
            return_value=Response(
                200,
                json={"project": sample_project_data},
            )
        )

        response = sonarqube_client.projects.create(
            name="My Project",
            project="my-project",
            visibility="private",
        )

        assert response.project.key == "my-project"
        assert response.project.name == "My Project"

    @respx.mock
    def test_delete(self, sonarqube_client: SonarQubeClient) -> None:
        """Test project deletion."""
        respx.post("/api/projects/delete").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.projects.delete(project="my-project")

    @respx.mock
    def test_update_key(self, sonarqube_client: SonarQubeClient) -> None:
        """Test project key update."""
        respx.post("/api/projects/update_key").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.projects.update_key(
            from_key="old-key",
            to_key="new-key",
        )

    @respx.mock
    def test_update_visibility(self, sonarqube_client: SonarQubeClient) -> None:
        """Test project visibility update."""
        respx.post("/api/projects/update_visibility").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.projects.update_visibility(
            project="my-project",
            visibility="public",
        )

    @respx.mock
    def test_bulk_delete(self, sonarqube_client: SonarQubeClient) -> None:
        """Test bulk project deletion."""
        respx.post("/api/projects/bulk_delete").mock(return_value=Response(204))

        # Should not raise
        sonarqube_client.projects.bulk_delete(
            projects=["project1", "project2"],
        )
