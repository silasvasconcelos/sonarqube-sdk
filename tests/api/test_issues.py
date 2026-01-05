"""Tests for Issues API."""

from __future__ import annotations

import respx
from httpx import Response

from sonarqube import SonarQubeClient
from sonarqube.models.issues import Issue, IssueSearchResponse


class TestIssuesAPI:
    """Tests for IssuesAPI."""

    @respx.mock
    def test_search(
        self,
        sonarqube_client: SonarQubeClient,
        sample_issue_data: dict,
        sample_paging_data: dict,
    ) -> None:
        """Test issues search."""
        respx.get("/api/issues/search").mock(
            return_value=Response(
                200,
                json={
                    "paging": sample_paging_data,
                    "issues": [sample_issue_data],
                },
            )
        )

        response = sonarqube_client.issues.search(
            project_keys=["my-project"],
            severities=["MAJOR"],
        )

        assert isinstance(response, IssueSearchResponse)
        assert len(response.issues) == 1
        assert response.issues[0].key == "AXoN-12345"
        assert response.issues[0].severity == "MAJOR"

    @respx.mock
    def test_search_with_multiple_filters(
        self,
        sonarqube_client: SonarQubeClient,
        sample_paging_data: dict,
    ) -> None:
        """Test issues search with multiple filters."""
        respx.get("/api/issues/search").mock(
            return_value=Response(
                200,
                json={
                    "paging": sample_paging_data,
                    "issues": [],
                },
            )
        )

        response = sonarqube_client.issues.search(
            project_keys=["my-project"],
            severities=["CRITICAL", "BLOCKER"],
            types=["BUG"],
            statuses=["OPEN"],
            resolved=False,
        )

        assert isinstance(response, IssueSearchResponse)

    @respx.mock
    def test_assign(
        self,
        sonarqube_client: SonarQubeClient,
        sample_issue_data: dict,
    ) -> None:
        """Test issue assignment."""
        sample_issue_data["assignee"] = "jdoe"
        respx.post("/api/issues/assign").mock(
            return_value=Response(
                200,
                json={"issue": sample_issue_data},
            )
        )

        issue = sonarqube_client.issues.assign(
            issue="AXoN-12345",
            assignee="jdoe",
        )

        assert isinstance(issue, Issue)
        assert issue.assignee == "jdoe"

    @respx.mock
    def test_add_comment(
        self,
        sonarqube_client: SonarQubeClient,
        sample_issue_data: dict,
    ) -> None:
        """Test adding comment to issue."""
        respx.post("/api/issues/add_comment").mock(
            return_value=Response(
                200,
                json={"issue": sample_issue_data},
            )
        )

        issue = sonarqube_client.issues.add_comment(
            issue="AXoN-12345",
            text="This is a comment",
        )

        assert isinstance(issue, Issue)

    @respx.mock
    def test_do_transition(
        self,
        sonarqube_client: SonarQubeClient,
        sample_issue_data: dict,
    ) -> None:
        """Test issue transition."""
        sample_issue_data["status"] = "RESOLVED"
        respx.post("/api/issues/do_transition").mock(
            return_value=Response(
                200,
                json={"issue": sample_issue_data},
            )
        )

        issue = sonarqube_client.issues.do_transition(
            issue="AXoN-12345",
            transition="resolve",
        )

        assert isinstance(issue, Issue)
        assert issue.status == "RESOLVED"

    @respx.mock
    def test_set_severity(
        self,
        sonarqube_client: SonarQubeClient,
        sample_issue_data: dict,
    ) -> None:
        """Test setting issue severity."""
        sample_issue_data["severity"] = "CRITICAL"
        respx.post("/api/issues/set_severity").mock(
            return_value=Response(
                200,
                json={"issue": sample_issue_data},
            )
        )

        issue = sonarqube_client.issues.set_severity(
            issue="AXoN-12345",
            severity="CRITICAL",
        )

        assert isinstance(issue, Issue)
        assert issue.severity == "CRITICAL"

    @respx.mock
    def test_set_tags(
        self,
        sonarqube_client: SonarQubeClient,
        sample_issue_data: dict,
    ) -> None:
        """Test setting issue tags."""
        sample_issue_data["tags"] = ["team-a", "priority"]
        respx.post("/api/issues/set_tags").mock(
            return_value=Response(
                200,
                json={"issue": sample_issue_data},
            )
        )

        issue = sonarqube_client.issues.set_tags(
            issue="AXoN-12345",
            tags=["team-a", "priority"],
        )

        assert isinstance(issue, Issue)
        assert issue.tags == ["team-a", "priority"]

    @respx.mock
    def test_bulk_change(
        self,
        sonarqube_client: SonarQubeClient,
    ) -> None:
        """Test bulk change issues."""
        respx.post("/api/issues/bulk_change").mock(
            return_value=Response(
                200,
                json={"total": 2, "success": 2, "ignored": 0, "failures": 0},
            )
        )

        result = sonarqube_client.issues.bulk_change(
            issues=["AXoN-12345", "AXoN-12346"],
            add_tags=["team-a"],
            assign="jdoe",
        )

        assert result["total"] == 2
        assert result["success"] == 2
