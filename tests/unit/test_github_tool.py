"""Unit tests for GitHubTool, focused on reproducing issue #50.

Reproduction for #50: GitHubTool's metadata dict has a `has_readme`
boolean field but no `has_tests` field, even for repos that clearly
have tests. This is documented here as a failing test rather than a
live API call, so it runs offline and isn't subject to GitHub's rate
limits.
"""

from unittest.mock import MagicMock, patch

import pytest

from agent.tools.github_tool import GitHubTool


@pytest.mark.unit
class TestGitHubToolHasTests:
    """Reproduction tests for missing has_tests field (#50)."""

    @pytest.fixture
    def tool(self) -> GitHubTool:
        """Create a GitHubTool instance."""
        return GitHubTool()

    @pytest.fixture
    def mock_repo_response(self) -> dict:
        """A minimal fake GitHub API repo response."""
        return {
            "name": "pathreview",
            "description": "AI-powered portfolio review assistant",
            "language": "Python",
            "stargazers_count": 0,
            "forks_count": 0,
            "open_issues_count": 0,
            "pushed_at": "2026-07-20T17:40:56Z",
            "topics": [],
            "homepage": "",
        }

    def test_metadata_has_no_has_tests_field(
        self, tool: GitHubTool, mock_repo_response: dict
    ) -> None:
        """Reproduction: has_tests is entirely absent from the metadata dict.

        Even though this repo has a tests/ directory at its root
        (confirmed manually), GitHubTool never checks for or reports
        this, unlike has_readme which is already implemented.
        """
        mock_repo_resp = MagicMock(status_code=200)
        mock_repo_resp.json.return_value = mock_repo_response
        mock_repo_resp.raise_for_status = MagicMock()

        mock_readme_resp = MagicMock(status_code=200)

        with patch("httpx.get", return_value=mock_repo_resp), \
             patch("httpx.head", return_value=mock_readme_resp):
            result = tool.execute({
                "github_username": "Alessandra005",
                "repo_name": "pathreview",
            })

        assert result.success is True
        assert "has_readme" in result.data  # sanity check: sibling field exists
        assert "has_tests" in result.data, (
            "Reproduction of #50: 'has_tests' key is missing from the "
            "metadata dict, even for a repo with a tests/ directory."
        )