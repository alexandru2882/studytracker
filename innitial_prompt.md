hey! i built you a **start-to-finish, no-stoppers tutorial** that gets you from “nothing installed” to a **working Python project you can run, test, and push to GitHub**—fast. we’ll keep explanations short, then do the thing immediately.

The mini project is a tiny CLI app called **studytracker**. You’ll add study sessions (topic + minutes), list them, and see a quick report. It uses only the Python standard library, so setup stays simple, and it’s structured to be portfolio-ready.&#x20;

---

# 0) Pick your OS and set up tools

We’ll install **Python 3.12+**, **Git**, and create an isolated environment (**venv**) so nothing breaks on your computer. Then we’ll install a few developer helpers: **pytest** (tests), **black**/**ruff** (format/lint), **mypy** (types). The flow follows your file’s “copy-pasteable, cross-platform” principle.&#x20;

### macOS (Terminal: bash/zsh)

```bash
# 1) Install Homebrew if you don't have it (paste, press Enter, follow prompts)
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2) Python + Git
brew install python@3.12 git

# 3) Make project folder
mkdir -p ~/code/studytracker && cd ~/code/studytracker

# 4) Virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 5) Upgrade packaging tools + dev helpers
python -m pip install --upgrade pip setuptools wheel
pip install -e . pytest mypy black ruff
```

### Linux (Debian/Ubuntu; use your terminal)

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
mkdir -p ~/code/studytracker && cd ~/code/studytracker
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e . pytest mypy black ruff
```

### Windows (PowerShell)

```powershell
# 1) Install Python + Git (if winget exists)
winget install --id Python.Python.3.12 -e
winget install --id Git.Git -e

# 2) Make project folder
mkdir $HOME\code\studytracker
Set-Location $HOME\code\studytracker

# 3) Virtual environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# If activation is blocked, run once:
# Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 4) Upgrade packaging tools + dev helpers
python -m pip install --upgrade pip setuptools wheel
pip install -e . pytest mypy black ruff
```

> Sanity checks:
>
> * On macOS/Linux: `python --version && pip --version`
> * On Windows: `py --version` (then use `python` inside the venv)

*(These OS-specific steps are aligned with your provided setup section.)*&#x20;

---

# 1) Scaffold the project

We’ll use a **src/** layout and set up packaging so the app installs a `studytracker` command. This mirrors the “portfolio-ready repo structure with tests and CI” goal.&#x20;

Create folders:

```bash
# macOS/Linux (Terminal)
mkdir -p src/studytracker tests .github/workflows
touch src/studytracker/__init__.py
```

```powershell
# Windows (PowerShell)
mkdir src\studytracker
mkdir tests
mkdir .github\workflows
New-Item src\studytracker\__init__.py -ItemType File | Out-Null
```

Now create these files **exactly** with the content below (open any editor and paste; or use VS Code if you have it with `code .`):

### `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "studytracker"
version = "0.1.0"
description = "Tiny CLI to track study sessions (topic + minutes)."
readme = "README.md"
requires-python = ">=3.12"
authors = [{name = "You"}]

[project.scripts]
studytracker = "studytracker.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.black]
line-length = 100

[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.12"
strict = false
```

### `README.md`

````markdown
# studytracker

A tiny cross-platform CLI to track what you study.

## Quickstart
```bash
# in project root
python -m pip install -e .
studytracker add "Python" 30
studytracker list
studytracker report
````

## Why this exists

Practice Python packaging, CLI, JSON storage, tests, and CI in one afternoon.

````

### `src/studytracker/models.py`
```python
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class StudySession:
    topic: str
    minutes: int
    date: str  # YYYY-MM-DD

    def __post_init__(self) -> None:
        if not isinstance(self.topic, str) or not self.topic.strip():
            raise ValueError("topic must be a non-empty string")
        if not isinstance(self.minutes, int) or self.minutes <= 0:
            raise ValueError("minutes must be a positive integer")
        # Very light date format check
        parts = self.date.split("-")
        if len(parts) != 3:
            raise ValueError("date must be YYYY-MM-DD")

    def to_dict(self) -> Dict[str, Any]:
        return {"topic": self.topic, "minutes": self.minutes, "date": self.date}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StudySession":
        return StudySession(topic=str(d["topic"]), minutes=int(d["minutes"]), date=str(d["date"]))
````

### `src/studytracker/storage.py`

```python
import json
import os
from pathlib import Path
from typing import List
from .models import StudySession

def _base_dir() -> Path:
    # Use env var for tests; default to user home
    env = os.getenv("STUDYTRACKER_HOME")
    p = Path(env).expanduser() if env else (Path.home() / ".studytracker")
    p.mkdir(parents=True, exist_ok=True)
    return p

def data_path() -> Path:
    return _base_dir() / "sessions.json"

def load_sessions() -> List[StudySession]:
    p = data_path()
    if not p.exists():
        return []
    raw = p.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    data = json.loads(raw)
    return [StudySession.from_dict(x) for x in data]

def save_sessions(items: List[StudySession]) -> None:
    p = data_path()
    p.write_text(json.dumps([s.to_dict() for s in items], indent=2), encoding="utf-8")
```

### `src/studytracker/logic.py`

```python
from datetime import date
from typing import List, Optional
from .models import StudySession
from .storage import load_sessions, save_sessions

def add_session(topic: str, minutes: int, when: Optional[str] = None) -> StudySession:
    if when is None:
        when = date.today().isoformat()
    session = StudySession(topic=topic, minutes=int(minutes), date=when)
    items = load_sessions()
    items.append(session)
    save_sessions(items)
    return session

def list_sessions() -> List[StudySession]:
    return load_sessions()

def total_minutes(topic: Optional[str] = None) -> int:
    items = load_sessions()
    if topic:
        items = [x for x in items if x.topic.lower() == topic.lower()]
    return sum(x.minutes for x in items)
```

### `src/studytracker/cli.py`

```python
import argparse
from .logic import add_session, list_sessions, total_minutes

def main() -> None:
    parser = argparse.ArgumentParser(prog="studytracker", description="Track study sessions")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a study session")
    p_add.add_argument("topic", type=str, help="What you studied")
    p_add.add_argument("minutes", type=int, help="Minutes spent (positive integer)")
    p_add.add_argument("--date", type=str, default=None, help="YYYY-MM-DD (default: today)")

    p_list = sub.add_parser("list", help="List sessions")

    p_report = sub.add_parser("report", help="Total minutes (optionally for a topic)")
    p_report.add_argument("--topic", type=str, default=None, help="Filter by topic")

    args = parser.parse_args()

    if args.cmd == "add":
        s = add_session(args.topic, args.minutes, args.date)
        print(f"Added: {s.topic} for {s.minutes} min on {s.date}")
    elif args.cmd == "list":
        items = list_sessions()
        if not items:
            print("No sessions yet.")
            return
        for i, s in enumerate(items, start=1):
            print(f"{i}. {s.date} — {s.topic}: {s.minutes} min")
    elif args.cmd == "report":
        total = total_minutes(args.topic)
        if args.topic:
            print(f"Total for '{args.topic}': {total} min")
        else:
            print(f"Total minutes: {total}")
```

### `tests/test_storage.py`

```python
import os
from studytracker.logic import add_session, list_sessions, total_minutes

def test_add_list_total(tmp_path, monkeypatch):
    # Redirect data to a temp folder so tests don't touch your real files
    monkeypatch.setenv("STUDYTRACKER_HOME", str(tmp_path))

    assert list_sessions() == []
    add_session("Python", 30, "2025-01-01")
    add_session("Math", 45, "2025-01-02")
    add_session("Python", 25, "2025-01-03")

    items = list_sessions()
    assert len(items) == 3
    assert total_minutes() == 100
    assert total_minutes("python") == 55
```

### `.github/workflows/ci.yml` (optional but recommended)

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --upgrade pip
      - run: pip install -e . pytest mypy black ruff
      - run: ruff check .
      - run: black --check .
      - run: mypy src/
      - run: pytest -q
```

*(This mirrors the “repo & CI” guidance in your file.)*&#x20;

---

# 2) Install your package locally

Back in your terminal (with the venv active):

```bash
python -m pip install -e .
```

This makes the `studytracker` command available on your machine (editable install), as suggested by your portfolio-ready packaging requirement.&#x20;

---

# 3) Verify with tests (fast feedback)

```bash
pytest -q
```

You should see all tests pass. If something fails, read the message—it’s precise. (Your plan emphasizes tiny, runnable checks and pytest; we’re doing exactly that.)&#x20;

---

# 4) Use the CLI (real, live project)

```bash
studytracker add "Python" 30
studytracker add "Math" 45 --date 2025-08-10
studytracker list
studytracker report
studytracker report --topic Python
```

Expected example output:

```
Added: Python for 30 min on 2025-08-11
Added: Math for 45 min on 2025-08-10
1. 2025-08-11 — Python: 30 min
2. 2025-08-10 — Math: 45 min
Total minutes: 75
Total for 'Python': 30 min
```

---

# 5) Format, lint, type-check (fast, optional polish)

```bash
ruff check .
black --check .
mypy src/
```

If `black --check` complains, auto-format with:

```bash
black .
```

(These match the “helpers and self-check commands” idea.)&#x20;

---

# 6) Initialize Git and push to GitHub

The file encourages a **public, CI-backed repo** with clear commits. Here’s the simplest path.&#x20;

```bash
git init
git add .
git commit -m "chore: initial scaffold for studytracker"
# OPTION A: if you have GitHub CLI (gh)
# gh repo create <your-username>/studytracker --public --source=. --push

# OPTION B: classic remote method
# 1) Create an empty repo named "studytracker" on GitHub in your browser.
# 2) Then run:
git branch -M main
git remote add origin https://github.com/<your-username>/studytracker.git
git push -u origin main
```

Once pushed, GitHub Actions (if you added `ci.yml`) will run your tests automatically on every push/PR.&#x20;

---

# 7) What you’ve just learned (quietly)

* **Python packaging** with `pyproject.toml` and a **console script** so `studytracker` works like a real tool.
* **CLI basics** with `argparse`.
* **JSON persistence** (read/write) cleanly separated into modules.
* **Tests** with `pytest` and temporary directories.
* **Formatting/linting/types** for professional hygiene.
  This aligns with the “syntax-first + project-backed” approach and the “capstone split into small lessons” intent—except we compressed it to ship a working MVP today with zero blockers.&#x20;

---

# 8) Zero-stopper tips

* **Windows venv activation**: if blocked, run once:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
* **Command not found after `pip install -e .`?** Re-activate your venv (`source .venv/bin/activate` or `.\.venv\Scripts\Activate.ps1`) and try again.
* **Tests touching your real data?** They don’t. We use `STUDYTRACKER_HOME` to redirect storage during tests.
* **Want to reset data?** Delete `~/.studytracker/sessions.json` (or the folder on Windows `C:\Users\<you>\.studytracker`).

---

# 9) Fast follow (optional, 30–60 min)

When you’re ready to grow the MVP, here’s the next bite-size path—each can be a commit/PR:

1. **Export to CSV/Markdown** (`studytracker report --csv`),
2. **Type hints to “strict”** and fix mypy warnings,
3. **Add streaks** (count consecutive days with any session).

These are consistent with the original capstone’s feature ideas and lesson-by-lesson growth plan.&#x20;

---

# 10) Want interactive practice next?

Your file also describes a **one-exercise-at-a-time engine** with Easy/Medium/Hard. I can run you through that now (e.g., Easy set on variables/functions, then fold changes back into this repo), track your score, and end with a stats summary and “next steps.” Say the word and I’ll start with Lesson 1.&#x20;

---

If you follow the steps above in order, you’ll go from clean machine → working CLI → tests/CI → public proof of skills—with minimal waiting and no detours. Ready to run the exercise session, or do you want me to auto-extend the CLI with CSV export first?
