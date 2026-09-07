# Spec: Login and Logout

## Overview
This feature implements user authentication for Spendly. It converts the `/login` stub (currently `GET`-only, rendering `templates/login.html` with no form handling) into a functional `GET`+`POST` route that verifies credentials against the `users` table, stores the authenticated user's ID in the session, and redirects to the landing page. It also implements the `/logout` placeholder, which currently returns the raw string `"Logout — coming in Step 3"`, replacing it with a route that clears the session and redirects to the landing page. After this step, the app can distinguish logged-in users from guests, which is a prerequisite for Step 4 (profile) and all expense features.

## Depends on
- Step 01 — Database Setup (`.claude/specs/01-database-setup.md`): requires `get_db()` and the `users` table.
- Step 02 — Registration (`.claude/specs/02-registration.md`): requires real user rows (with hashed passwords) to authenticate against; `login.html` already renders a `registered=1` success message from this step.

## Routes
- `GET /login` — render login form — public
- `POST /login` — validate credentials, set session, redirect — public
- `GET /logout` — clear session, redirect to `/` — public (no login required to log out)

## Database changes
No database changes. The `users` table created in Step 01 already stores `email` and `password_hash`.

## Templates
- **Create:** none
- **Modify:** `templates/login.html` — the `<form>` already `POST`s to `/login` with `email`/`password` fields and already displays `error` and the `registered` success message (added in Step 02). Only change needed: none required for markup — if a failed login needs to re-populate `email` (not `password`), add a `value="{{ email }}"` attribute to the email input, mirroring `register.html`'s pattern.

## Files to change
- `app.py` — replace the `GET`-only `login()` with a `GET`+`POST` handler (`methods=["GET", "POST"]`); replace the `logout()` placeholder body
- `database/db.py` — add `get_user_by_email(email)` helper that returns a user row or `None`
- `templates/login.html` — re-populate `email` value on failed login (see above)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is available via the existing `werkzeug` install (already used for `generate_password_hash` in `database/db.py`).

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting/f-strings to build SQL
- Passwords hashed with werkzeug — verify with `werkzeug.security.check_password_hash` against the stored `password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session key for the logged-in user must be `session["user_id"]` (integer)
- Use `flask.session` — do not roll a custom session mechanism; `app.secret_key` must be set for sessions to work (add if missing)
- `get_user_by_email` belongs in `database/db.py`, not inline in the route
- Normalize email to lowercase/stripped before lookup, consistent with Step 02's registration storage
- On failed login (unknown email or wrong password) show a single generic error ("Invalid email or password.") with HTTP 400 — do not reveal which field was wrong
- On success, redirect to `url_for("landing")` (no dashboard route exists yet)
- `logout()` must call `session.clear()` then redirect to `url_for("landing")`
- Do not modify unrelated routes, templates, or styles (e.g. leave `/profile`, `/expenses/*` placeholders untouched)

## Definition of done
- [ ] Visiting `GET /login` renders the login form with email and password fields (unchanged from today)
- [ ] Submitting the form with valid credentials (e.g. `demo@spendly.com` / `demo123`, seeded by `seed_db()`) sets `session["user_id"]` and redirects to `/`
- [ ] Submitting with a wrong password shows "Invalid email or password." and stays on the login page with HTTP 400
- [ ] Submitting with an unregistered email shows the same generic error
- [ ] Visiting `GET /logout` clears the session and redirects to `/`
- [ ] After logout, `session["user_id"]` is no longer present
- [ ] `/logout` no longer returns the raw placeholder string
- [ ] App starts and existing routes (`/`, `/register`, `/terms`, `/privacy`) continue to work without errors
