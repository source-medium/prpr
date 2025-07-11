"""GitHub CLI wrapper for prpr."""

import json
import shutil
import subprocess
from typing import Any


class GitHubAPI:
    """Wrapper around GitHub CLI (gh) for API operations."""

    def is_available(self) -> bool:
        """Check if GitHub CLI is available in PATH."""
        return shutil.which("gh") is not None

    def get_current_pr_number(self) -> int | None:
        """Get PR number from current branch."""
        try:
            # First try to get PR number from current branch
            result = subprocess.run(
                ["gh", "pr", "view", "--json", "number"],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(result.stdout)
            return data.get("number")
        except subprocess.CalledProcessError:
            # Try to extract from branch name if it's a PR branch
            try:
                result = subprocess.run(
                    ["git", "symbolic-ref", "--short", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                branch = result.stdout.strip()

                # Check if branch matches refs/pull/123/head pattern
                if branch.startswith("refs/pull/") and branch.endswith("/head"):
                    pr_num = branch.split("/")[2]
                    return int(pr_num)

            except (subprocess.CalledProcessError, ValueError, IndexError):
                pass

            return None

    def get_pr_comments(self, pr_number: int) -> list[dict[str, Any]]:
        """Fetch all comments for a PR."""
        try:
            # Get PR review comments
            result = subprocess.run(
                [
                    "gh",
                    "api",
                    f"repos/{{owner}}/{{repo}}/pulls/{pr_number}/comments",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            comments = json.loads(result.stdout)

            # Transform to our format
            transformed_comments = []
            for comment in comments:
                transformed_comments.append(
                    {
                        "id": f"THR_{comment['id']}",
                        "file": comment.get("path", ""),
                        "line": comment.get("line", 0),
                        "state": "open",  # GitHub API doesn't provide resolved state directly
                        "author_login": comment["user"]["login"],
                        "body": comment["body"],
                        "created_at": comment["created_at"],
                    }
                )

            return transformed_comments

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to fetch PR comments: {e}")

    def post_reply(self, thread_id: str, message: str) -> str:
        """Post a reply to a thread."""
        try:
            # Extract comment ID from thread ID
            comment_id = thread_id.replace("THR_", "")

            # Use gh api to post reply
            result = subprocess.run(
                [
                    "gh",
                    "api",
                    f"repos/{{owner}}/{{repo}}/pulls/comments/{comment_id}/replies",
                    "--method",
                    "POST",
                    "--field",
                    f"body={message}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            response = json.loads(result.stdout)
            return str(response["id"])

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to post reply: {e}")
