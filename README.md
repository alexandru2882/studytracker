# studytracker

Track what you study, in minutes, from the command line. Minimal dependencies, fast to set up, and designed as a small but complete portfolio-quality Python project.

## What it does

- **Add sessions**: Log a topic and how many minutes you studied, optionally with a specific date.
- **List sessions**: See a chronological list of everything you've logged.
- **Report totals**: View total minutes across all topics, or filtered to a single topic.

Under the hood, studytracker stores your data in a simple JSON file on your machine, so there’s nothing to configure and no external services to rely on.

## Why this exists

- **Build real-world muscle**: It demonstrates packaging with `pyproject.toml`, a console entrypoint, clean module structure, and tests.
- **Practical habit tool**: A quick way to track focused study time without switching context to a GUI.
- **Zero-dependency runtime**: Uses only the Python standard library for simple, reliable persistence.

## How it works

The code is organized into small modules:

- `models.py`: Defines the `StudySession` data model with lightweight validation.
- `storage.py`: Reads/writes sessions as JSON to a data file in your home directory (or a custom path via env var).
- `logic.py`: Business logic for adding, listing, and aggregating sessions.
- `cli.py`: The command-line interface powered by `argparse`.

By default, data is stored at `~/.studytracker/sessions.json`. For tests or custom setups, set `STUDYTRACKER_HOME` to change the base directory.

## Installation

Requirements: Python 3.12+

```bash
# from the project root
python -m pip install -e .
```

This installs a console command named `studytracker`.

## Usage

```bash
# Add sessions (default date is today)
studytracker add "Python" 30
studytracker add "Math" 45 --date 2025-08-10

# List what you've logged
studytracker list

# Totals across all topics
studytracker report

# Totals for a single topic (case-insensitive)
studytracker report --topic Python
```

Example output:

```
Added: Python for 30 min on 2025-08-11
Added: Math for 45 min on 2025-08-10
1. 2025-08-11 — Python: 30 min
2. 2025-08-10 — Math: 45 min
Total minutes: 75
Total for 'Python': 30 min
```

## Configuration

- **Data location**: Set `STUDYTRACKER_HOME` to point storage somewhere else (useful for tests or portable setups).
  - Default: `~/.studytracker/sessions.json`
- **Date format**: `YYYY-MM-DD`. If omitted, today’s date is used.

## Development

Helpful commands (optional but recommended):

```bash
# Run tests
pytest -q

# Lint and format
ruff check .
black .

# Type-check
mypy src/
```

## Roadmap ideas

- CSV/Markdown export of reports
- Stricter type hints and mypy configuration
- Streak tracking (consecutive study days)

## License

MIT (or your preferred license). Replace this section if you adopt a different license.

