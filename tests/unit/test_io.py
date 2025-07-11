"""Unit tests for io module."""

import tempfile

import pytest

from prpr.io import ThreadsIO


class TestThreadsIO:
    """Test JSON I/O operations."""

    def test_write_and_read_threads(self):
        """Test writing and reading threads data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            threads_io = ThreadsIO(temp_dir)

            threads = [
                {
                    "id": "THR_123",
                    "file": "src/app.py",
                    "line": 42,
                    "state": "open",
                    "author_login": "alice",
                    "author_type": "teammate",
                    "body": "Good work!",
                    "created_at": "2025-07-09T12:34:56Z",
                },
            ]

            # Write threads
            threads_io.write_threads(123, threads)

            # Check file exists
            assert threads_io.threads_exist()

            # Read threads
            data = threads_io.read_threads()

            assert data["schema_version"] == "0.1.0"
            assert data["pr"] == 123
            assert len(data["threads"]) == 1
            assert data["threads"][0]["id"] == "THR_123"
            assert "updated_at" in data

    def test_read_nonexistent_file(self):
        """Test reading non-existent threads file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            threads_io = ThreadsIO(temp_dir)

            with pytest.raises(FileNotFoundError):
                threads_io.read_threads()

    def test_threads_exist_false(self):
        """Test threads_exist returns False when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            threads_io = ThreadsIO(temp_dir)
            assert not threads_io.threads_exist()
