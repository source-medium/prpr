"""Comment classification logic for prpr."""

import re
from typing import Any

from prpr.config import Config


class CommentClassifier:
    """Classifies GitHub PR comments by author type."""

    def __init__(self, config: Config):
        """Initialize classifier with configuration.

        Args:
            config: Configuration object with ai_author_patterns
        """
        self.config = config

    def classify_author_type(self, author_login: str) -> str:
        """Classify author type based on login name.

        Args:
            author_login: GitHub username

        Returns:
            Author type: 'self', 'teammate', or 'ai_bot'
        """
        # Check if author matches AI patterns
        ai_patterns = self.config.ai_author_patterns
        for pattern in ai_patterns:
            if self._matches_pattern(author_login, pattern):
                return "ai_bot"

        # For now, classify all non-AI authors as teammates
        # In a real implementation, we'd need to determine the current user
        # and classify as 'self' vs 'teammate' accordingly
        return "teammate"

    def _matches_pattern(self, author_login: str, pattern: str) -> bool:
        """Check if author login matches a pattern.

        Args:
            author_login: GitHub username
            pattern: Pattern to match (supports basic wildcards)

        Returns:
            True if pattern matches
        """
        # Convert pattern to regex and escape special characters
        regex_pattern = re.escape(pattern).replace("\\*", ".*")
        return bool(re.match(regex_pattern, author_login, re.IGNORECASE))

    def classify_comments(self, comments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Classify a list of comments.

        Args:
            comments: List of comment dictionaries

        Returns:
            List of comments with author_type added
        """
        classified_comments = []

        for comment in comments:
            classified_comment = comment.copy()
            classified_comment["author_type"] = self.classify_author_type(
                comment["author_login"],
            )
            classified_comments.append(classified_comment)

        return classified_comments
