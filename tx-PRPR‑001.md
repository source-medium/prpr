## Ticket PRPR‑001 — MVP **prpr** CLI (agent‑ready)

*Status:* Open | Priority  High | Owner  Claude Code (autonomous agent)
*Target tag:* `v0.1.0` (MVP) | Repo: `github.com/your‑org/prpr`

---

### 1 . Objective

Build the first usable cut of **prpr**, a Python CLI that lets humans *and* agents pull, classify, and act on GitHub pull‑request comments.
Only four verbs are required for v0.1:

| Verb                                          | Purpose                                                                     |
| --------------------------------------------- | --------------------------------------------------------------------------- |
| `prpr sync`                                   | Fetch all threads/comments for the current PR ➜ write `.prpr/threads.json`. |
| `prpr ls`                                     | Emit a filtered JSON list to **stdout**.                                    |
| `prpr reply <thread‑id> "<msg>"`              | Post a reply.                                                               |
| (Nice‑to‑have) `prpr check-new --since <ISO>` | List comments newer than timestamp.                                         |

No live “watch”, no scoring engine, no multi‑VCS.

---

### 2 . Functional spec — *MUST* pass

| # | Behaviour            | Acceptance test (CI)                                                                              | Expected result                                                                |
| - | -------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1 | **Dependency guard** | Run `prpr sync` with no `gh` binary in `$PATH`.                                                   | Exit code `9`; stderr contains­ `"GitHub CLI not found"`.                      |
| 2 | **Detect PR**        | In a cloned repo checked out to `refs/pull/123/head`, run `prpr sync`.                            | `.prpr/threads.json` created; top‑level `pr` field equals `123`.               |
| 3 | **Classification**   | Feed the fixture `tests/data/sample_gh.json` to the sync routine (mocked `gh api`).               | Every item has `author_type` ∈ *self/teammate/ai\_bot* following rules in cfg. |
| 4 | **Filtering**        | `prpr ls --author ai_bot --open --json` on the same fixture.                                      | JSON array length =`2` (exact match in fixture).                               |
| 5 | **Reply**            | `prpr reply THR_FIX "LGTM"` (mocked post).                                                        | CLI prints returned comment ID; exit code `0`.                                 |
| 6 | **Config loading**   | Create `tests/tmp/home/.prpr.toml` with `ai_author_patterns = ["renovate[bot]"]`; run classifier. | Comment by *renovate\[bot]* tagged `ai_bot` (was `teammate` before).           |

> **Coverage gate:** unit+integration tests ≥ 90 % lines (`pytest‑cov`). CI fails below.

---

### 3 . JSON schema (authoritative for v0.1)

```jsonc
{
  "schema_version": "0.1.0",
  "pr": 123,
  "updated_at": "2025-07-10T18:00:00Z",
  "threads": [
    {
      "id": "THR_abc123",
      "file": "src/app.py",
      "line": 42,
      "state": "open",          // "open" | "resolved"
      "author_login": "alice",
      "author_type": "teammate",// "self" | "teammate" | "ai_bot"
      "body": "Nit: rename var",
      "created_at": "2025‑07‑09T12:34:56Z"
    }
  ]
}
```

*Any field addition/removal in future versions must bump `schema_version`.*

---

### 4 . Directory layout to implement

```
prpr/
├─ prpr/
│  ├─ __main__.py      # Typer entry
│  ├─ gh.py            # thin wrapper around `gh api`
│  ├─ classifier.py    # pure logic, unit‑tested
│  ├─ io.py            # read/write JSON
│  └─ config.py        # ~/.prpr.toml loader
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ data/sample_gh.json
├─ pyproject.toml      # Poetry
└─ .github/workflows/ci.yml
```

---

### 5 . Done‑Definition checklist (agent must satisfy **all**)

* [ ] All six CI tests in §2 green on GitHub Actions.
* [ ] `prpr --help` shows the four verbs with options.
* [ ] README △ *Quick‑start* section that passes when copy‑pasted.
* [ ] `pipx install .` succeeds on Python 3.10 & 3.11 in CI matrix.
* [ ] License file = MIT.
* [ ] Code formatted by `ruff` & `black`, checked in CI.
* [ ] Coverage badge added to README.

---

### 6 . Development hints for Claude Code

* **Mocking `gh`:** tests must not hit real GitHub. Use `pytest-mock` to stub `subprocess.run`.
* **Fixtures:** `tests/data/sample_gh.json` already resembles a medium‑size PR (20 threads, mix of bots).
* **Exit codes:** reserve 0 = success, 9 = missing dependency, 10 = API failure, 11 = invalid args.
* **Timebox:** aim for two working days coding, one day tests/docs.

---

### 7 . Nice‑to‑have (implement only if ahead of schedule)

* `prpr check-new --since <ISO>`
* Emoji priority mapping (🔥/⚠️) added to classifier.

---

