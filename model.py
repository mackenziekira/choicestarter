"""Models and database functions for Poetry project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



############################################################################
# Model definitions

class Individual(db.Model):
    """class for individual objects"""

    __tablename__ = 'individuals'


    individual_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    poem_url = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    tsv = db.Column(TSVECTOR)


    author = db.relationship('Author', backref='poems')
    subjects = db.relationship('Subject', secondary='poems_subjects', backref='poems')

    def __repr__(self):
        """repr for a more readable poem object"""
        return "{}".format(self.title.encode('unicode-escape'))



if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print 'connected to db'