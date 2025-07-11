"""Integration tests for CLI commands."""

import json
import tempfile
from unittest.mock import patch

from click.testing import CliRunner

from prpr.__main__ import cli


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("prpr.gh.GitHubAPI.is_available")
    def test_sync_no_gh_cli(self, mock_is_available):
        """Test sync command when GitHub CLI is not available."""
        mock_is_available.return_value = False

        result = self.runner.invoke(cli, ["sync"])

        assert result.exit_code == 9
        assert "GitHub CLI not found" in result.stderr

    @patch("prpr.gh.GitHubAPI.is_available")
    @patch("prpr.gh.GitHubAPI.get_current_pr_number")
    @patch("prpr.gh.GitHubAPI.get_pr_comments")
    def test_sync_success(self, mock_get_comments, mock_get_pr, mock_is_available):
        """Test successful sync command."""
        mock_is_available.return_value = True
        mock_get_pr.return_value = 123
        mock_get_comments.return_value = [
            {
                "id": "THR_123",
                "file": "src/app.py",
                "line": 42,
                "state": "open",
                "author_login": "alice",
                "body": "Good work!",
                "created_at": "2025-07-09T12:34:56Z",
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("prpr.io.ThreadsIO.__init__", return_value=None):
                with patch("prpr.io.ThreadsIO.write_threads") as mock_write:
                    result = self.runner.invoke(cli, ["sync"])

                    assert result.exit_code == 0
                    assert "Synced 1 threads for PR #123" in result.stdout
                    mock_write.assert_called_once()

    def test_ls_no_threads_file(self):
        """Test ls command when threads file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("prpr.io.ThreadsIO.__init__", return_value=None):
                with patch(
                    "prpr.io.ThreadsIO.read_threads", side_effect=FileNotFoundError
                ):
                    result = self.runner.invoke(cli, ["ls"])

                    assert result.exit_code == 10
                    assert "Failed to read threads" in result.stderr

    def test_ls_with_filters(self):
        """Test ls command with filters."""
        threads_data = {
            "schema_version": "0.1.0",
            "pr": 123,
            "updated_at": "2025-07-10T18:00:00Z",
            "threads": [
                {
                    "id": "THR_1",
                    "author_type": "teammate",
                    "state": "open",
                    "body": "Good work!",
                },
                {
                    "id": "THR_2",
                    "author_type": "ai_bot",
                    "state": "open",
                    "body": "Update dependency",
                },
                {
                    "id": "THR_3",
                    "author_type": "ai_bot",
                    "state": "resolved",
                    "body": "Coverage report",
                },
            ],
        }

        with patch("prpr.io.ThreadsIO.__init__", return_value=None):
            with patch("prpr.io.ThreadsIO.read_threads", return_value=threads_data):
                # Test author filter
                result = self.runner.invoke(cli, ["ls", "--author", "ai_bot", "--json"])
                assert result.exit_code == 0
                output = json.loads(result.stdout)
                assert len(output) == 2

                # Test open filter
                result = self.runner.invoke(
                    cli, ["ls", "--author", "ai_bot", "--open", "--json"]
                )
                assert result.exit_code == 0
                output = json.loads(result.stdout)
                assert len(output) == 1
                assert output[0]["id"] == "THR_2"

    @patch("prpr.gh.GitHubAPI.is_available")
    def test_reply_no_gh_cli(self, mock_is_available):
        """Test reply command when GitHub CLI is not available."""
        mock_is_available.return_value = False

        result = self.runner.invoke(cli, ["reply", "THR_123", "LGTM"])

        assert result.exit_code == 9
        assert "GitHub CLI not found" in result.stderr

    @patch("prpr.gh.GitHubAPI.is_available")
    @patch("prpr.gh.GitHubAPI.post_reply")
    def test_reply_success(self, mock_post_reply, mock_is_available):
        """Test successful reply command."""
        mock_is_available.return_value = True
        mock_post_reply.return_value = "9876543210"

        result = self.runner.invoke(cli, ["reply", "THR_123", "LGTM"])

        assert result.exit_code == 0
        assert "9876543210" in result.stdout
        mock_post_reply.assert_called_once_with("THR_123", "LGTM")

    def test_check_new_no_since(self):
        """Test check-new command without --since parameter."""
        result = self.runner.invoke(cli, ["check-new"])

        assert result.exit_code == 2  # Click returns 2 for missing required options
        assert "Missing option" in result.output

    def test_check_new_with_since(self):
        """Test check-new command with --since parameter."""
        threads_data = {
            "schema_version": "0.1.0",
            "pr": 123,
            "updated_at": "2025-07-10T18:00:00Z",
            "threads": [
                {
                    "id": "THR_1",
                    "body": "Old comment",
                    "created_at": "2025-07-09T10:00:00Z",
                },
                {
                    "id": "THR_2",
                    "body": "New comment",
                    "created_at": "2025-07-09T14:00:00Z",
                },
            ],
        }

        with patch("prpr.io.ThreadsIO.__init__", return_value=None):
            with patch("prpr.io.ThreadsIO.read_threads", return_value=threads_data):
                result = self.runner.invoke(
                    cli, ["check-new", "--since", "2025-07-09T12:00:00Z"]
                )

                assert result.exit_code == 0
                output = json.loads(result.stdout)
                assert len(output) == 1
                assert output[0]["id"] == "THR_2"
