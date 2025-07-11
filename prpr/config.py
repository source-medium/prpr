"""Configuration loader for prpr."""

from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    import toml as tomllib


class Config:
    """Configuration loader for prpr settings."""

    def __init__(self, config_path: str = None):
        """Initialize config loader.

        Args:
            config_path: Path to config file. Defaults to ~/.prpr.toml
        """
        if config_path is None:
            config_path = Path.home() / ".prpr.toml"
        else:
            config_path = Path(config_path)

        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from TOML file."""
        if not self.config_path.exists():
            return {}

        try:
            if hasattr(tomllib, "load"):
                with open(self.config_path, "rb") as f:
                    return tomllib.load(f)
            else:
                # toml library uses text mode
                with open(self.config_path) as f:
                    return tomllib.load(f)
        except Exception:
            return {}

    @property
    def ai_author_patterns(self) -> list[str]:
        """Get AI author patterns for classification."""
        return self._config.get(
            "ai_author_patterns",
            [
                "dependabot[bot]",
                "renovate[bot]",
                "github-actions[bot]",
                "bot",
            ],
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self._config.get(key, default)
