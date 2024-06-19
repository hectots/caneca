# caneca

Another Flask + HTMX + Tailwind boilerplate. This is a "single" file Flask setup for quick prototyping and simple apps.

# Features

- Tailwind + daisyUI.
- DB migrations with Flyway-style setup.
- Login with Google OAuth.
- Invite-only access to users.
- Manager script with commands for running migrations and accepting users.
- Procfile for PaaS such as Heroku.
- HTMX included.

# Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install requirements.txt
echo "
GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
GOOGLE_CLIENT_SECRET=<your-google-oauth-client-secret>
DATABASE_URL=postgresql://<user>:<pass>@<host>:<port>/<db>
" > .env
npm install
npm run create-css
flask --name app run
```

# Details

## DB and migrations

There's a `db` module where you can put your data access layer. It follows the write-your-own-sql philosophy but you can add SQLAlchemy if you want.

Migrations are handled via SQL scripts in the `db/migrations` directory. The script should follow the naming convention `V<version>__Description.sql`, replacing `<version>` with the actual version. I like to use timestamps for the versions but that is not required. Executing the `manage.py migrate` command will migrate the DB to the latest version.

## Login and user management

There are routes for login and authentication using authlib. It is preconfigured to user Google OAuth but can be easily changed by editing the `oauth.register()` lines in `app.py`.

To secure your routes add the `@require_login` decorator to them. The "members only" page is and example of this:

```python
@app.route('/members')
@require_login
def view_members_only():
    return render_template("members.html", user=session.get('user'))
```

Logged-in users will not have immediate access to secured routes. They will instead enter in a "pending users" area. To accept users use the `manage.py accept` command.

## Tailwind + daisyUI and templating

Tailwind and daisyUI setup is handled by an script you can run with `npm run create-css`. A base template is provided with `templates/base.html`, which includes the CSS and JS bundles provided by Flask-Assets. HTMX is included by default.
