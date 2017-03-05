"""Models and database functions for Choice Starter project"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


############################################################################
# Model definitions

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer , primary_key=True)
    username = db.Column('username', db.Text(), unique=True, index=True)
    password = db.Column('password' , db.Text())
    email = db.Column('email', db.Text())
    registered_on = db.Column('registered_on', db.DateTime)
    stripe_id = db.Column('stripe_id', db.Text(), index=True)

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_stripe(self, stripe):
        self.stripe_id = stripe

    def __repr__(self):
        return '<User %r>' % (self.username)


class Organization(db.Model):
    """class for individual objects"""

    __tablename__ = 'orgs'

    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text())
    location = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text())
    phone = db.Column(db.Text())
    address = db.Column(db.Text())
    approved = db.Column(db.Boolean, nullable=False)
    template_featured = db.Column(db.Integer, unique=True, index=True)
    template_hero_image = db.Column(db.LargeBinary)

    def __init__(self, name, description, location, email, phone):
        self.name = name
        self.description = description
        self.location = location
        self.email = email
        self.phone = phone
        self.approved = False

    def __repr__(self):
        """repr for a more readable organization object"""
        return "{}".format(self.name.encode('unicode-escape'))


# All possible roles, e.g. donor, admin, viewer
class Role(db.Model):
    __tablename__ = 'roles'

    role = db.Column('role', db.Text(), primary_key=True)

    def __init__(self, role):
        self.role = role


class UserRole(db.Model):
    __tablename__ = 'userroles'

    userrole_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('orgs.org_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role = db.Column(db.Text(), db.ForeignKey('roles.role'), nullable=False)

    def __init__(self, org_id, user_id, role):
        self.org_id = org_id
        self.user_id = user_id
        self.role = role



#############################################################################

# Helper functions

def connect_to_db(app):
    """Connect the database to Flask application"""

    db.init_app(app)
    db.app = app

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print 'connected to db'