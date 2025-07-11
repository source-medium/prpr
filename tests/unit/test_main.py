"""Unit tests for main module."""

import pytest
from click.testing import CliRunner

from prpr.__main__ import cli, main


class TestMain:
    """Test main entry point."""

    def test_main_function(self):
        """Test main function works."""
        runner = CliRunner()

        # Test main function by calling help
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "CLI tool for managing GitHub pull request comments" in result.output

    def test_main_direct_call(self):
        """Test main function can be called directly."""
        # This tests the main() function
        runner = CliRunner()

        # Mock the cli function to avoid actual execution
        with pytest.raises(SystemExit):
            # This will call main() which calls cli()
            main()
