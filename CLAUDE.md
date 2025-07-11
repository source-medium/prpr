# prpr CLI Development Guide

## Project Overview
**prpr** is a Python CLI tool for managing GitHub pull request comments, designed to be both human and AI agent friendly. This MVP (v0.1.0) focuses on four core commands: `sync`, `ls`, `reply`, and `check-new`.

## Technical Requirements

### Core Commands
- `prpr sync` - Fetch PR threads and create `.prpr/threads.json`
- `prpr ls` - Filter and display threads as JSON to stdout
- `prpr reply <thread-id> "<msg>"` - Post replies to GitHub
- `prpr check-new --since <ISO>` - List new comments (nice-to-have)

### Architecture
- **Python 3.10+** with Poetry for dependency management
- **Typer** for CLI interface
- **GitHub CLI (`gh`)** as external dependency
- **JSON-based** data storage and API communication
- **TOML configuration** in `~/.prpr.toml`

### Directory Structure (Required)
```
prpr/
├─ prpr/
│  ├─ __main__.py      # Typer entry point
│  ├─ gh.py            # GitHub CLI wrapper
│  ├─ classifier.py    # Comment classification logic
│  ├─ io.py            # JSON read/write operations
│  └─ config.py        # Configuration loader
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ data/sample_gh.json
├─ pyproject.toml      # Poetry configuration
└─ .github/workflows/ci.yml
```

## Development Guidelines

### Exit Codes
- `0` - Success
- `9` - Missing dependency (GitHub CLI not found)
- `10` - API failure
- `11` - Invalid arguments

### JSON Schema (v0.1.0)
```json
{
  "schema_version": "0.1.0",
  "pr": 123,
  "updated_at": "2025-07-10T18:00:00Z",
  "threads": [
    {
      "id": "THR_abc123",
      "file": "src/app.py",
      "line": 42,
      "state": "open",
      "author_login": "alice",
      "author_type": "teammate",
      "body": "Nit: rename var",
      "created_at": "2025-07-09T12:34:56Z"
    }
  ]
}
```

### Comment Classification
Author types: `self`, `teammate`, `ai_bot`
- Configuration via `~/.prpr.toml` with `ai_author_patterns` array
- Default patterns should include common bot names

### Testing Requirements
- **90%+ test coverage** (enforced by CI)
- **Unit tests** for all core logic
- **Integration tests** for CLI commands
- **Mocked GitHub API** calls (no real API hits in tests)
- **pytest-cov** for coverage reporting

## Quality Standards

### Code Formatting
- **ruff** for linting
- **black** for code formatting
- Both checked in CI pipeline

### CI/CD Requirements
- **GitHub Actions** workflow
- **Python 3.10 & 3.11** test matrix
- **Coverage reporting** with badge
- **All 6 acceptance tests** must pass

### Documentation
- **README** with quick-start section
- **MIT License** file
- **Coverage badge** in README
- **Help text** for all commands

## Development Commands

### Setup
```bash
poetry install
poetry run prpr --help
```

### Testing
```bash
poetry run pytest --cov=prpr tests/
poetry run pytest tests/unit/
poetry run pytest tests/integration/
```

### Code Quality
```bash
poetry run ruff check prpr/
poetry run black --check prpr/
poetry run ruff format prpr/
poetry run black prpr/
```

## Key Implementation Notes

1. **GitHub CLI Dependency**: Always check for `gh` binary in PATH
2. **PR Detection**: Must work with `refs/pull/123/head` checkout
3. **Configuration**: Support `~/.prpr.toml` for user preferences
4. **Error Handling**: Proper exit codes and error messages
5. **JSON Output**: Clean, parseable JSON for machine consumption

## Repository
- **GitHub**: `source-medium/prpr`
- **License**: MIT
- **Python**: 3.10+
- **Installation**: `pipx install .`

## Done Definition Checklist
- [ ] All six CI tests pass on GitHub Actions
- [ ] `prpr --help` shows all four verbs with options
- [ ] README quick-start section works when copy-pasted
- [ ] `pipx install .` succeeds on Python 3.10 & 3.11
- [ ] MIT license file present
- [ ] Code formatted by ruff & black, checked in CI
- [ ] Coverage badge added to README