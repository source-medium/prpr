"""Unit tests for classifier module."""

from prpr.classifier import CommentClassifier
from prpr.config import Config


class TestCommentClassifier:
    """Test comment classification logic."""

    def test_classify_ai_bot(self):
        """Test AI bot classification."""
        config = Config()
        classifier = CommentClassifier(config)

        # Test default AI patterns
        assert classifier.classify_author_type("dependabot[bot]") == "ai_bot"
        assert classifier.classify_author_type("renovate[bot]") == "ai_bot"
        assert classifier.classify_author_type("github-actions[bot]") == "ai_bot"
        assert classifier.classify_author_type("bot") == "ai_bot"

    def test_classify_teammate(self):
        """Test teammate classification."""
        config = Config()
        classifier = CommentClassifier(config)

        # Test human usernames
        assert classifier.classify_author_type("alice-dev") == "teammate"
        assert classifier.classify_author_type("bob-reviewer") == "teammate"
        assert classifier.classify_author_type("charlie") == "teammate"

    def test_classify_comments_batch(self):
        """Test batch classification of comments."""
        config = Config()
        classifier = CommentClassifier(config)

        comments = [
            {"author_login": "alice-dev", "body": "Good work!"},
            {"author_login": "renovate[bot]", "body": "Update dependency"},
            {"author_login": "bob-reviewer", "body": "LGTM"},
        ]

        classified = classifier.classify_comments(comments)

        assert len(classified) == 3
        assert classified[0]["author_type"] == "teammate"
        assert classified[1]["author_type"] == "ai_bot"
        assert classified[2]["author_type"] == "teammate"

    def test_custom_ai_patterns(self):
        """Test custom AI patterns from config."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test.toml"
            config_path.write_text(
                """
ai_author_patterns = ["custom-bot", "special[bot]"]
"""
            )

            config = Config(str(config_path))
            classifier = CommentClassifier(config)

            assert classifier.classify_author_type("custom-bot") == "ai_bot"
            assert classifier.classify_author_type("special[bot]") == "ai_bot"
            assert classifier.classify_author_type("renovate[bot]") == "teammate"
