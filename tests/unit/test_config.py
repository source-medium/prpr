"""Unit tests for config module."""

import tempfile
from pathlib import Path

from prpr.config import Config


class TestConfig:
    """Test configuration loading."""

    def test_default_config_empty(self):
        """Test default config when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "nonexistent.toml"
            config = Config(str(config_path))

            assert config.ai_author_patterns == [
                "dependabot[bot]",
                "renovate[bot]",
                "github-actions[bot]",
                "bot",
            ]

    def test_config_with_ai_patterns(self):
        """Test loading config with ai_author_patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test.toml"
            config_path.write_text(
                """
ai_author_patterns = ["renovate[bot]", "custom-bot"]
"""
            )

            config = Config(str(config_path))
            assert config.ai_author_patterns == ["renovate[bot]", "custom-bot"]

    def test_config_get_method(self):
        """Test generic get method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test.toml"
            config_path.write_text(
                """
custom_key = "custom_value"
"""
            )

            config = Config(str(config_path))
            assert config.get("custom_key") == "custom_value"
            assert config.get("nonexistent", "default") == "default"
