"""JSON I/O operations for prpr."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ThreadsIO:
    """Handles reading and writing threads JSON data."""

    def __init__(self, threads_dir: str = ".prpr"):
        """Initialize with threads directory.

        Args:
            threads_dir: Directory to store threads.json
        """
        self.threads_dir = Path(threads_dir)
        self.threads_file = self.threads_dir / "threads.json"

    def write_threads(self, pr_number: int, threads: list[dict[str, Any]]) -> None:
        """Write threads data to JSON file.

        Args:
            pr_number: PR number
            threads: List of thread dictionaries
        """
        # Ensure directory exists
        self.threads_dir.mkdir(exist_ok=True)

        # Create threads data structure
        threads_data = {
            "schema_version": "0.1.0",
            "pr": pr_number,
            "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "threads": threads,
        }

        # Write to file
        with open(self.threads_file, "w") as f:
            json.dump(threads_data, f, indent=2)

    def read_threads(self) -> dict[str, Any]:
        """Read threads data from JSON file.

        Returns:
            Threads data dictionary

        Raises:
            FileNotFoundError: If threads.json doesn't exist
        """
        if not self.threads_file.exists():
            raise FileNotFoundError(f"Threads file not found: {self.threads_file}")

        with open(self.threads_file) as f:
            return json.load(f)

    def threads_exist(self) -> bool:
        """Check if threads file exists."""
        return self.threads_file.exists()
