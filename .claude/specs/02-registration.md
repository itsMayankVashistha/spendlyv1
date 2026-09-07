# Registration

## Overview

Implement user registration for Spendly. Currently `/register` (in `app.py`) only renders `templates/register.html`, which already posts `name`, `email`, and `password` fields to `/register` but nothing handles the `POST`. This step wires that form up to the `users` table created in Step 1 (`.claude/specs/01-database-setup.md`), so a visitor can create an account, gets validated/duplicate-checked, and is redirected to log in.

This step does **not** implement login/session handling (Step 3) — a successful registration redirects to the login page rather than logging the user in directly.

## Dependencies

- Depends on [Step 1 — Database Setup](01-database-setup.md): requires `get_db()`, `init_db()`, and the `users` table to already exist.
- No other feature steps depend on registration being complete except login (Step 3), which needs real user rows to authenticate against.

## Routes to Implement

### `POST /register` (extend existing `GET /register`)

- `GET /register` — unchanged, renders the empty form.
- `POST /register` — new handling on the same route:
    - Read `name`, `email`, `password` from `request.form`.
    - Validate:
        - All three fields required (non-empty after `.strip()`).
        - `password` must be at least 8 characters.
        - `email` must not already exist in `users` (case-insensitive compare recommended, e.g. store/compare lowercased).
    - On validation failure:
        - Re-render `register.html` with `error` set to a user-facing message and HTTP 400.
        - Do not leak whether an email exists beyond "An account with this email already exists."
    - On success:
        - Hash the password with `werkzeug.security.generate_password_hash`.
        - Insert a new row into `users` via a parameterized `INSERT`.
        - Redirect (`302`) to `/login`, optionally with a flash-style query param or flashed message indicating success (e.g. "Account created — please sign in").

## Database Changes

None. The `users` table (from Step 1) already has the required columns: `id`, `name`, `email` (unique), `password_hash`, `created_at`. No migrations needed.

## Templates to Create / Modify

- `templates/register.html` — modify:
    - Keep existing markup/fields as-is (already correct).
    - Ensure the `{% if error %}` block continues to display server-side validation errors.
    - Re-populate `name`/`email` input `value` attributes after a failed submission so the user doesn't have to retype them (do **not** re-populate `password`).
- `templates/login.html` — modify (small):
    - Support displaying an optional success message (e.g. from a query param or flashed message) after redirect from registration, consistent with how `register.html` shows `error`.

## Files Modified

- `app.py` — add `POST` handling to the `/register` route (`methods=["GET", "POST"]`), import `request` and `redirect`/`url_for` from Flask if not already imported.
- `templates/register.html` — re-populate fields on error.
- `templates/login.html` — show optional success message after registration redirect.

## New Files Created

None.

## New Dependencies

None. Uses only what's already available:
- `flask` (`request`, `redirect`, `url_for`, `render_template`)
- `werkzeug.security.generate_password_hash` (already used in `database/db.py`)
- `database.db.get_db`

## Rules of Implementation

- No ORMs — use raw `sqlite3` via `get_db()`, as established in Step 1.
- **Parameterized queries only** — never use string formatting/f-strings to build SQL.
- Always hash passwords with `generate_password_hash`; never store plaintext.
- Treat email uniqueness as case-insensitive: normalize (`.lower()`) before comparing/storing, or rely on the `UNIQUE` constraint but catch `sqlite3.IntegrityError` as a fallback safety net.
- Close DB connections after use (or rely on existing per-request connection pattern already used in the codebase).
- Follow CLAUDE.md conventions: plain Jinja2/vanilla JS/CSS only, no new frontend frameworks; don't touch unrelated templates, styles, or routes (e.g. leave `/logout`, `/profile`, `/expenses/*` placeholders untouched).
- Keep page-specific styling in existing stylesheets; do not introduce new CSS files for this step unless a genuinely new UI element requires it.

## Acceptance Criteria (Definition of Done)

- [ ] `GET /register` still renders the form unchanged.
- [ ] `POST /register` with valid, unique data creates a new row in `users` with a hashed password and redirects to `/login`.
- [ ] `POST /register` with a missing field re-renders the form with an appropriate error and no DB write occurs.
- [ ] `POST /register` with a password under 8 characters re-renders the form with an appropriate error.
- [ ] `POST /register` with an email that already exists re-renders the form with a clear error and no duplicate row is created.
- [ ] Submitted `name`/`email` values are preserved in the form after a failed submission; `password` is not.
- [ ] All SQL is parameterized; no string-formatted queries.
- [ ] `login.html` can display an optional success message after a successful registration redirect.
- [ ] No unrelated routes, templates, or styles are modified.
- [ ] App starts and existing routes (`/`, `/login`, `/terms`, `/privacy`) continue to work without errors.
