import base64
from io import BytesIO
import uuid

from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, url_for, redirect, g, request, session
from flask_assets import Bundle, Environment
from PIL import ImageDraw

from db.user import is_new_user, add_pending_user
from security.access import require_login


app = Flask(__name__)
app.secret_key = 'X4h6SKNzci'
app.config.from_object('config')

assets = Environment(app)
css = Bundle("src/main.css",  output="css/main.css")
js = Bundle("src/*.js", output="js/main.js")

assets.register("css", css)
assets.register("js", js)
css.build()
js.build()

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route("/")
def homepage():
    user = session.get('user')
    return render_template("index.html", user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user = token['userinfo']

    if is_new_user(user['sub']):
        add_pending_user(user)
        return redirect('/pending-user')
    else:
        session['user'] = user
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/pending-user')
def show_pending_user_welcome_message():
    return render_template("pending-user.html")


@app.route('/members')
@require_login
def view_members_only():
    return render_template("members.html", user=session.get('user'))


if __name__ == "__main__":
    app.run(debug=True)
