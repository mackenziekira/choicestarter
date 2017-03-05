from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session, g
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


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/organizations')
def organizations():
    return render_template("organizations.html")


@app.route('/donate')
def donate():
    return render_template("donate.html")


@app.route('/account')
@login_required
def account():
    return render_template("account.html")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # POST request, trying to login
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter(User.username == username).first()
    if registered_user is None:
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        return redirect(url_for('login'))
    login_user(registered_user, remember=False)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 


@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    # Post request
    existing_user = User.query.filter(User.username == request.form['username']).first()
    if existing_user:
        message = "Sorry, that username is already taken."
        return render_template('register.html', message=message)
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=False)
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


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