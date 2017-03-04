from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from model import db, connect_to_db
import os

app = Flask(__name__)

# Raises an error if you use undefined Jinja variable.
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    """Homepage."""

    return render_template("landingpage.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # app.config['SQLALCHEMY_ECHO'] = True

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "asdf9k$")

    # Required to use Flask sessions and the debug toolbar
    app.secret_key = SECRET_KEY


    app.jinja_env.auto_reload = True
    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=PORT, debug=DEBUG)