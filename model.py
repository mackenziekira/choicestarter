"""Models and database functions for Poetry project"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


############################################################################
# Model definitions

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password' , db.String(250))
    email = db.Column('email', db.String(50), unique=True , index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    role = db.Column('role' , db.String(250))

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()
        self.role = role

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

    def __repr__(self):
        return '<User %r>' % (self.username)



class Organization(db.Model):
    """class for individual objects"""

    __tablename__ = 'organizations'


    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(700), nullable=False)
    location = db.Column(db.String(700), nullable=False)

    def __repr__(self):
        """repr for a more readable organization object"""
        return "{}".format(self.name.encode('unicode-escape'))

#############################################################################

# Helper functions

def connect_to_db(app, db_uri=None):
    """Connect the database to Flask application"""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or "postgresql:///choicestarter"
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print 'connected to db'