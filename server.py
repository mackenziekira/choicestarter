from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session, g, url_for, flash, make_response
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
# from model import db, connect_to_db
from model import *
import os
import config
from payments import create_charge, create_transfer, create_user, charge_customer

application = Flask(__name__)
app = application
app.config.from_object(config)

# Raises an error if you use undefined Jinja variable.
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    """Homepage."""
    # If logged in
    # find all roles
    # pass all roles and data to landing page
    featured_3_organizations = Organization.query.filter(Organization.template_featured <= 3)
    return render_template("landingpage.html", featured_3_organizations=featured_3_organizations)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/manage_orgs')
def manage_orgs():
    return render_template("manage_orgs.html")


@app.route('/my_donations')
def my_donations():
    return render_template("my_donations.html")


@app.route('/organizations')
def organizations():
    return render_template("organizations.html")

@app.route('/organizations/<org_id>')
def organization(org_id):
    organization = Organization.query.filter(Organization.org_id == org_id).first()
    return render_template('organization.html', organization=organization)


@app.route('/organizations/<org_id>/hero_image')
def organization_template_hero_image(org_id):
    organization = Organization.query.filter(Organization.org_id == org_id).first()
    response = make_response(organization.template_hero_image)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@app.route('/donate')
def donate():
    return render_template("donate.html", no_payment_saved=((not g.user.is_authenticated) or (g.user.stripe_id is None)))


@app.route('/account')
@login_required
def account():
    return render_template("account.html")


@app.route('/forgot_password')
def forgot_password():
    return render_template("forgot_password.html")


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message=None)


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter(User.username == username).first()
    if registered_user is None:
        return redirect(url_for('login_get'))
    if not registered_user.check_password(password):
        return redirect(url_for('login_get'))
    login_user(registered_user, remember=False)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register_donor' , methods=['GET','POST'])
def register_donor():
    if request.method == 'GET':
        return render_template('register_donor.html', message=None)
    # Post request
    existing_user = User.query.filter(User.username == request.form['username']).first()
    if existing_user:
        msg = "Sorry, that username is already taken."
        return render_template('register_donor.html', message=msg)
    role = 'donor'
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.flush()
    login_user(user, remember=False)
    # Add donor role
    role = 'donor'
    userrole = UserRole(None, g.user.id, role)
    db.session.add(userrole)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/register_org' , methods=['GET'])
def register_org_get():
    if g.user.is_authenticated:
        return render_template('register_org.html', message=None)
    else:
        flash("Register your organization.")
        return redirect(url_for('login_get'))


@app.route('/register_org' , methods=['POST'])
def register_org_post():
    existing_org = Organization.query.filter(Organization.name == request.form['name']).first()
    if existing_org:
        msg = "Sorry, that organization name is already taken."
        return render_template('register_org.html', message=msg)
    # Create organization
    org = Organization(request.form['name'], request.form['description'], request.form['location'],
        request.form['email'], request.form['phone'])
    db.session.add(org)
    db.session.flush()
    # Add org-admin user-role
    role = 'admin'
    userrole = UserRole(org.org_id, g.user.id, role)
    db.session.add(userrole)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/charge', methods=['POST'])
def charge():
    amount = request.form['amount']

    if g.user.is_authenticated:
        registered_user = User.query.filter(User.id == g.user.id).first()
        stripe_id = registered_user.stripe_id
        if stripe_id is None:
            print "case 1"
            token = request.form['stripeToken']
            customer = create_user(token)
            registered_user.set_stripe(customer)
            #db.session.update(registered_user)
            db.session.commit()
        else:
            print "case 2"
            customer = registered_user.stripe_id
        charged = charge_customer(customer, amount)
    else:
        print "case 3"
        print(request)
        print(request.form)
        token = request.form['stripeToken']
        amount = request.form['amount']
        charged = create_charge(amount, token)
    return '<h1>'+charged.outcome.type+'</h1>'


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
    connect_to_db(app)
    # os.environ.get("DATABASE_URL")

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=PORT, debug=DEBUG)
