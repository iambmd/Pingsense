# PingSense

Website to search for equipment and tutorials, from beginner to professional table tennis.

PingSense is a data-driven hub for table tennis players: a Flask-powered site with user accounts, a rubber equipment database, and curated YouTube learning resources.

## Contents

- [`app.py`](app.py) - the Flask application: routes for the landing page, the Learn page, the `/learn/recommendation` API, and user registration/login/logout.
- [`templates/`](templates/) - Jinja templates for each page:
  - `index.html` - the landing page, with a hero section and equipment/database highlights.
  - `learn.html` - "Learn From the Best", fetches its channel cards client-side from `/learn/recommendation`.
  - `login.html` / `register.html` - the auth forms.
- [`data/table_tennis_rubbers.csv`](data/table_tennis_rubbers.csv) - dataset of 984 table tennis rubbers across 52 brands, sourced from real user reviews on [revspin.net](https://revspin.net/rubber/). Each rubber lists Price and 0-10 scale ratings for Speed, Spin, Tackiness, and Overall. Rubbers with 3 or fewer user ratings were excluded to keep the data statistically meaningful.

## Running the site

Requires Python 3.9+.

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows (PowerShell: .venv\Scripts\Activate.ps1)
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python app.py
```

The site is served at `http://127.0.0.1:5000`. A SQLite database (`instance/pingsense.db`) is created automatically on first run to store user accounts.

Set a real `SECRET_KEY` environment variable before deploying anywhere beyond local dev — the app falls back to an insecure default key otherwise:

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

## Accounts

Users can sign up with a username, email, and password (`/register`), then log in/out (`/login`, `/logout`). Passwords are hashed with Werkzeug's `generate_password_hash`; sessions are managed by Flask-Login; forms are CSRF-protected via Flask-WTF.

## Data source

The rubber dataset is a standalone CSV asset (not yet wired into a page) intended for future features like searchable/filterable equipment tables or rubber comparisons. Data was compiled from [revspin.net/rubber](https://revspin.net/rubber/), a community-driven table tennis equipment review site, filtered to rubbers with more than 3 user ratings.
