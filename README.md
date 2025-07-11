# prpr

[![CI](https://github.com/source-medium/prpr/actions/workflows/ci.yml/badge.svg)](https://github.com/source-medium/prpr/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/source-medium/prpr/branch/main/graph/badge.svg)](https://codecov.io/gh/source-medium/prpr)

A Python CLI tool for managing GitHub pull request comments - designed to be both human and AI agent friendly.

## Features

- **Sync PR comments** - Fetch all threads/comments for the current PR
- **Filter threads** - List comments by author type, state, or custom criteria
- **Reply to comments** - Post replies directly from the command line
- **Check for new comments** - Find comments newer than a specific timestamp
- **Agent-ready** - JSON output and structured data for AI automation

## Quick Start

### Installation

```bash
pipx install prpr
```

Or with pip:

```bash
pip install prpr
```

### Prerequisites

- Python 3.10 or higher
- GitHub CLI (`gh`) installed and authenticated
- Working in a GitHub repository with pull requests

### Basic Usage

1. **Sync PR comments to local storage:**
   ```bash
   prpr sync
   ```

2. **List all comments:**
   ```bash
   prpr ls --json
   ```

3. **Filter comments by author type:**
   ```bash
   prpr ls --author ai_bot --json
   ```

4. **Show only open threads:**
   ```bash
   prpr ls --open --json
   ```

5. **Reply to a comment:**
   ```bash
   prpr reply THR_1234567890 "Thanks for the review!"
   ```

6. **Check for new comments since a timestamp:**
   ```bash
   prpr check-new --since 2025-07-09T12:00:00Z
   ```

### Configuration

Create a `~/.prpr.toml` file to customize behavior:

```toml
ai_author_patterns = [
    "dependabot[bot]",
    "renovate[bot]",
    "github-actions[bot]",
    "codecov[bot]",
    "custom-bot"
]
```

## Commands

### `prpr sync`

Fetches all threads/comments for the current PR and saves them to `.prpr/threads.json`.

**Requirements:**
- Must be in a Git repository
- Must be on a PR branch or have GitHub CLI able to detect the current PR
- GitHub CLI must be installed and authenticated

**Exit codes:**
- `0` - Success
- `9` - GitHub CLI not found
- `10` - API failure
- `11` - Invalid arguments or not in a PR branch

### `prpr ls [OPTIONS]`

Lists and filters PR comments.

**Options:**
- `--author TEXT` - Filter by author type (`self`, `teammate`, `ai_bot`)
- `--open` - Show only open (unresolved) threads
- `--json` - Output as JSON (default shows abbreviated format)

**Examples:**
```bash
# Show all AI bot comments as JSON
prpr ls --author ai_bot --json

# Show only open threads
prpr ls --open

# Show open AI bot comments
prpr ls --author ai_bot --open --json
```

### `prpr reply THREAD_ID MESSAGE`

Posts a reply to a specific comment thread.

**Arguments:**
- `THREAD_ID` - The thread ID (e.g., `THR_1234567890`)
- `MESSAGE` - The reply message

**Example:**
```bash
prpr reply THR_1234567890 "LGTM! Thanks for the fix."
```

### `prpr check-new --since TIMESTAMP`

Lists comments created after the specified timestamp.

**Options:**
- `--since TEXT` - ISO timestamp (e.g., `2025-07-09T12:00:00Z`)

**Example:**
```bash
prpr check-new --since 2025-07-09T12:00:00Z
```

## Data Format

Comments are stored in `.prpr/threads.json` with the following structure:

```json
{
  "schema_version": "0.1.0",
  "pr": 123,
  "updated_at": "2025-07-10T18:00:00Z",
  "threads": [
    {
      "id": "THR_1234567890",
      "file": "src/app.py",
      "line": 42,
      "state": "open",
      "author_login": "alice",
      "author_type": "teammate",
      "body": "This could be improved...",
      "created_at": "2025-07-09T12:34:56Z"
    }
  ]
}
```

## Development

### Setup

```bash
git clone https://github.com/source-medium/prpr.git
cd prpr
poetry install
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=prpr

# Run specific test types
poetry run pytest tests/unit/
poetry run pytest tests/integration/
```

### Code Quality

```bash
# Format code
poetry run black prpr/
poetry run ruff format prpr/

# Check linting
poetry run ruff check prpr/
poetry run black --check prpr/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and coverage is ≥90%
6. Submit a pull request

## Roadmap

- [ ] Support for multiple VCS platforms
- [ ] Comment scoring and priority system
- [ ] Live watch mode for new comments
- [ ] Integration with popular code review tools
- [ ] Enhanced filtering and search capabilities