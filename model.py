"""Models and database functions for Poetry project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



############################################################################
# Model definitions

class Individual(db.Model):
    """class for individual objects"""

    __tablename__ = 'individuals'


    individual_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.org_id'))
    name = db.Column(db.String(500), nullable=False)
    age = db.Column(db.Integer)
    date_of_procedure = db.Column(db.Date)
    conception_date = db.Column(db.Date)

    subjects = db.relationship('Organization', backref='individuals')

    def __repr__(self):
        """repr for a more readable individual object"""
        return "{}".format(self.name.encode('unicode-escape'))

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