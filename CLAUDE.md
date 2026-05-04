# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands
- **Install dependencies**: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- **Run the application**: `source venv/bin/activate && python app.py` (listens on `http://127.0.0.1:5001`)
- **Run the test suite**: `source venv/bin/activate && pytest`
- **Run a single test**: `source venv/bin/activate && pytest path/to/test_file.py::test_name`
- **Refresh the virtual environment** (e.g., after changing `requirements.txt`): delete the `venv` folder and repeat the install step.

## High‑Level Architecture
- **Entry point** – `app.py` creates a Flask application and defines the primary public routes (`/`, `/register`, `/login`, `/terms`, `/privacy`). Placeholder routes for logout, profile, and expense management are scaffolded for later steps.
- **Templates** – Jinja2 HTML files live in `templates/` (`base.html` provides the common layout; other pages extend it). Static assets such as CSS and JavaScript are under `static/`.
- **Database layer** – The `database/` package is intended to hold SQLite helpers. `database/db.py` currently only contains comments describing the required functions:
  - `get_db()` – returns a connection with `row_factory` and foreign‑key enforcement.
  - `init_db()` – creates tables if they do not exist.
  - `seed_db()` – inserts development sample data.
- **Future work** – Students will implement the database helpers and the CRUD routes under `/expenses/…`. The architecture expects the Flask app to import these helpers and use them in the route handlers.

## Important Files & Directories
- `app.py` – Flask app definition and route registrations.
- `templates/` – HTML views rendered by Flask.
- `static/` – CSS (`style.css`) and JavaScript (`main.js`).
- `database/` – Package for SQLite interaction; currently a stub.
- `requirements.txt` – Pinning of Flask, Werkzeug, pytest, and pytest‑flask.

## Testing Notes
- The repository includes `pytest` and `pytest-flask`. Tests should import the Flask app from `app.py` and use the `client` fixture provided by `pytest-flask`.
- When adding new routes or database functions, add corresponding tests under a `tests/` directory (if created) and ensure they run with the `pytest` command.

## Additional Guidance for Claude Code
- When a task mentions “implement X” and references the database, check `database/db.py` for the expected function signatures.
- For UI changes, edit the appropriate Jinja template and, if needed, update the static assets.
- Use the virtual environment (`source venv/bin/activate`) before any Python command to guarantee the correct dependencies.
- Avoid modifying files outside the repository root; all changes should stay within the listed directories.
