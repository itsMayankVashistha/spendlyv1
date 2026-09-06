# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask-based personal expense tracker, built incrementally as a step-by-step learning project. Many pieces are intentionally left as placeholders (see "Current state" below) for future steps rather than being unfinished bugs.

## Commands

Dependency management uses `uv` (see `pyproject.toml` / `uv.lock`), with `requirements.txt` kept as an alternative.

```bash
# install deps (uv)
uv sync

# install deps (pip alternative)
pip install -r requirements.txt

# run the dev server (http://localhost:5001)
python app.py
# or
uv run app.py

# run tests
pytest
# run a single test file / test
pytest tests/test_foo.py
pytest tests/test_foo.py::test_bar
```

There is no lint/format tooling configured yet.

## Architecture

- `app.py` — single Flask app instance with all routes defined directly on it (no blueprints). Routes render templates via `render_template`; several routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) are placeholders returning plain strings, awaiting later implementation steps.
- `database/db.py` — intended to hold `get_db()` (SQLite connection, row_factory + foreign keys enabled), `init_db()` (CREATE TABLE IF NOT EXISTS), and `seed_db()` (sample data). Not yet implemented — currently just a comment describing the expected contents.
- `templates/` — Jinja2 templates. `base.html` defines the shared layout (navbar, footer, font/CSS includes) with `title`/`head`/`content`/`scripts` blocks; page templates (`landing.html`, `login.html`, `register.html`, `terms.html`, `privacy.html`) extend it. New pages should extend `base.html` rather than duplicating markup.
- `static/css/style.css` — shared/base styles (layout, navbar, footer, typography). `static/css/landing.css` — styles specific to the landing page (e.g. hero section). Keep this separation: page-specific styling goes in its own stylesheet, not into `style.css`.
- `static/js/main.js` — currently empty (placeholder); vanilla JS only, no frontend framework or bundler is used in this project.

## Conventions to follow

- No JS frameworks/bundlers, no CSS frameworks — plain Jinja2 templates, plain CSS, vanilla JS.
- When adding a new page: add a route in `app.py`, create a template extending `base.html`, and wire up any nav/footer links to the new route (avoid leaving `href="#"` placeholders once the real route exists).
- When asked to touch only one section/page, don't modify unrelated templates, styles, or routes.
