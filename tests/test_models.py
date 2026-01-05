"""Tests for Pydantic models."""

from __future__ import annotations

from sonarqube.models.common import Branch, Component, Paging, Project, Visibility
from sonarqube.models.issues import Issue, IssueSearchResponse
from sonarqube.models.projects import ProjectComponent, ProjectSearchResponse


class TestPaging:
    """Tests for Paging model."""

    def test_create(self) -> None:
        """Test Paging creation."""
        paging = Paging(pageIndex=1, pageSize=100, total=250)
        assert paging.page_index == 1
        assert paging.page_size == 100
        assert paging.total == 250

    def test_total_pages(self) -> None:
        """Test total_pages calculation."""
        paging = Paging(pageIndex=1, pageSize=100, total=250)
        assert paging.total_pages == 3

    def test_total_pages_exact_division(self) -> None:
        """Test total_pages when total is exact multiple of page_size."""
        paging = Paging(pageIndex=1, pageSize=100, total=200)
        assert paging.total_pages == 2

    def test_total_pages_zero_page_size(self) -> None:
        """Test total_pages with zero page_size."""
        paging = Paging(pageIndex=1, pageSize=0, total=100)
        assert paging.total_pages == 0

    def test_has_next_page(self) -> None:
        """Test has_next_page property."""
        paging = Paging(pageIndex=1, pageSize=100, total=250)
        assert paging.has_next_page is True

        paging = Paging(pageIndex=3, pageSize=100, total=250)
        assert paging.has_next_page is False

    def test_has_previous_page(self) -> None:
        """Test has_previous_page property."""
        paging = Paging(pageIndex=1, pageSize=100, total=250)
        assert paging.has_previous_page is False

        paging = Paging(pageIndex=2, pageSize=100, total=250)
        assert paging.has_previous_page is True


class TestVisibility:
    """Tests for Visibility enum."""

    def test_values(self) -> None:
        """Test Visibility enum values."""
        assert Visibility.PUBLIC == "public"
        assert Visibility.PRIVATE == "private"


class TestComponent:
    """Tests for Component model."""

    def test_create(self) -> None:
        """Test Component creation."""
        component = Component(
            key="my-project",
            name="My Project",
            qualifier="TRK",
            visibility="private",
        )
        assert component.key == "my-project"
        assert component.name == "My Project"
        assert component.qualifier == "TRK"
        assert component.visibility == "private"


class TestProject:
    """Tests for Project model."""

    def test_create(self) -> None:
        """Test Project creation."""
        project = Project(
            key="my-project",
            name="My Project",
            qualifier="TRK",
            visibility="private",
        )
        assert project.key == "my-project"
        assert project.name == "My Project"

    def test_create_with_alias(self) -> None:
        """Test Project creation with alias fields."""
        project = Project(
            key="my-project",
            name="My Project",
            lastAnalysisDate="2025-01-01T12:00:00+0000",
        )
        assert project.last_analysis_date == "2025-01-01T12:00:00+0000"


class TestBranch:
    """Tests for Branch model."""

    def test_create(self) -> None:
        """Test Branch creation."""
        branch = Branch(name="main", isMain=True, type="LONG")
        assert branch.name == "main"
        assert branch.is_main is True
        assert branch.type == "LONG"


class TestIssue:
    """Tests for Issue model."""

    def test_create(self) -> None:
        """Test Issue creation."""
        issue = Issue(
            key="AXoN-12345",
            rule="python:S1234",
            severity="MAJOR",
            component="my-project:src/main.py",
            project="my-project",
            message="Remove this unused variable",
            status="OPEN",
            type="CODE_SMELL",
        )
        assert issue.key == "AXoN-12345"
        assert issue.rule == "python:S1234"
        assert issue.severity == "MAJOR"

    def test_create_with_optional_fields(self) -> None:
        """Test Issue creation with optional fields."""
        issue = Issue(
            key="AXoN-12345",
            rule="python:S1234",
            component="my-project:src/main.py",
            project="my-project",
        )
        assert issue.severity is None
        assert issue.message is None


class TestProjectSearchResponse:
    """Tests for ProjectSearchResponse model."""

    def test_create(self) -> None:
        """Test ProjectSearchResponse creation."""
        response = ProjectSearchResponse(
            paging=Paging(pageIndex=1, pageSize=100, total=1),
            components=[
                ProjectComponent(
                    key="my-project",
                    name="My Project",
                    qualifier="TRK",
                )
            ],
        )
        assert response.paging.total == 1
        assert len(response.components) == 1
        assert response.components[0].key == "my-project"


class TestIssueSearchResponse:
    """Tests for IssueSearchResponse model."""

    def test_create(self) -> None:
        """Test IssueSearchResponse creation."""
        response = IssueSearchResponse(
            paging=Paging(pageIndex=1, pageSize=100, total=1),
            issues=[
                Issue(
                    key="AXoN-12345",
                    rule="python:S1234",
                    component="my-project:src/main.py",
                    project="my-project",
                )
            ],
        )
        assert len(response.issues) == 1
        assert response.issues[0].key == "AXoN-12345"
