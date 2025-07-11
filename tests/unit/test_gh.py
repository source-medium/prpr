"""Unit tests for gh module."""

import json
import subprocess
from unittest.mock import Mock, patch

import pytest

from prpr.gh import GitHubAPI


class TestGitHubAPI:
    """Test GitHub API wrapper."""

    @patch("shutil.which")
    def test_is_available_true(self, mock_which):
        """Test GitHub CLI availability check returns True."""
        mock_which.return_value = "/usr/local/bin/gh"

        gh_api = GitHubAPI()
        assert gh_api.is_available() is True
        mock_which.assert_called_once_with("gh")

    @patch("shutil.which")
    def test_is_available_false(self, mock_which):
        """Test GitHub CLI availability check returns False."""
        mock_which.return_value = None

        gh_api = GitHubAPI()
        assert gh_api.is_available() is False
        mock_which.assert_called_once_with("gh")

    @patch("subprocess.run")
    def test_get_current_pr_number_success(self, mock_run):
        """Test successful PR number retrieval."""
        mock_run.return_value = Mock(
            stdout='{"number": 123}',
            returncode=0,
        )

        gh_api = GitHubAPI()
        pr_number = gh_api.get_current_pr_number()

        assert pr_number == 123
        mock_run.assert_called_once_with(
            ["gh", "pr", "view", "--json", "number"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    def test_get_current_pr_number_failure(self, mock_run):
        """Test PR number retrieval failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["gh"])

        gh_api = GitHubAPI()
        pr_number = gh_api.get_current_pr_number()

        assert pr_number is None

    @patch("subprocess.run")
    def test_get_pr_comments_success(self, mock_run):
        """Test successful PR comments retrieval."""
        mock_comments = [
            {
                "id": 1234567890,
                "user": {"login": "alice"},
                "body": "Great work!",
                "created_at": "2025-07-09T12:34:56Z",
                "path": "src/app.py",
                "line": 42,
            },
        ]

        mock_run.return_value = Mock(
            stdout=json.dumps(mock_comments),
            returncode=0,
        )

        gh_api = GitHubAPI()
        comments = gh_api.get_pr_comments(123)

        assert len(comments) == 1
        assert comments[0]["id"] == "THR_1234567890"
        assert comments[0]["author_login"] == "alice"
        assert comments[0]["body"] == "Great work!"
        assert comments[0]["file"] == "src/app.py"
        assert comments[0]["line"] == 42
        assert comments[0]["state"] == "open"

    @patch("subprocess.run")
    def test_get_pr_comments_failure(self, mock_run):
        """Test PR comments retrieval failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["gh"])

        gh_api = GitHubAPI()

        with pytest.raises(RuntimeError, match="Failed to fetch PR comments"):
            gh_api.get_pr_comments(123)

    @patch("subprocess.run")
    def test_post_reply_success(self, mock_run):
        """Test successful reply posting."""
        mock_run.return_value = Mock(
            stdout='{"id": 9876543210}',
            returncode=0,
        )

        gh_api = GitHubAPI()
        comment_id = gh_api.post_reply("THR_1234567890", "LGTM")

        assert comment_id == "9876543210"
        mock_run.assert_called_once_with(
            [
                "gh",
                "api",
                "repos/{owner}/{repo}/pulls/comments/1234567890/replies",
                "--method",
                "POST",
                "--field",
                "body=LGTM",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    def test_post_reply_failure(self, mock_run):
        """Test reply posting failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["gh"])

        gh_api = GitHubAPI()

        with pytest.raises(RuntimeError, match="Failed to post reply"):
            gh_api.post_reply("THR_1234567890", "LGTM")
