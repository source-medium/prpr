"""Unit tests for config edge cases."""

import tempfile
from pathlib import Path

from prpr.config import Config


class TestConfigEdgeCases:
    """Test configuration edge cases."""

    def test_config_with_invalid_toml(self):
        """Test config with invalid TOML file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "invalid.toml"
            config_path.write_text("invalid [ toml content")

            config = Config(str(config_path))

            # Should fall back to defaults
            assert config.ai_author_patterns == [
                "dependabot[bot]",
                "renovate[bot]",
                "github-actions[bot]",
                "bot",
            ]

    def test_config_with_empty_file(self):
        """Test config with empty file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "empty.toml"
            config_path.write_text("")

            config = Config(str(config_path))

            # Should fall back to defaults
            assert config.ai_author_patterns == [
                "dependabot[bot]",
                "renovate[bot]",
                "github-actions[bot]",
                "bot",
            ]
