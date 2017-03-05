from model import connect_to_db, db 
from model import Individual, Organization
from server import app
import os

def load_organizations():
    """loads organizations into db"""

    orgs = [['The Lilith Fund', 'Texas'], ['Women\'s Medical Fund', 'Maryland'], ['Vermont Access to Reproductive Freedom', 'Vermont']]
    for org in orgs:
        organization = Organization(name=org[0],
                        location=org[1])
        db.session.add(organization)
    db.session.commit()

def load_individuals():
    """load individuals into database"""

    title = Parse.parse_title(soup)
    body = Parse.parse_poem(soup)
    author_id = author.author_id

    poem = Poem(title=title,
        body=body,
        poem_url="",
        author_id=author_id,
        tsv=tsv)

    db.session.add(poem)
    db.session.commit()

def load_subjects(soup, poem):
    """loads subjects from poem meta tags"""
    poem_id = poem.poem_id

    subjects = Parse.parse_subjects(soup)

    if subjects:
        for subject in subjects:
            try:
                subject_id = Subject.query.filter(Subject.subject_name == subject).one().subject_id
            except NoResultFound:
                log_err('subject', f, subject)
                s = Subject(subject_name=subject)
                db.session.add(s)
                db.session.flush()
                subject_id = s.subject_id
            

            poemsubject = PoemSubject(poem_id=poem_id,
                                        subject_id=subject_id)

            db.session.add(poemsubject)

            db.session.flush()





if __name__ == "__main__":
    connect_to_db(app)

    # drop all tables
    db.drop_all()

    # clear the error logging file
    e = open('err', 'w')
    e.close()

    # create all tables
    db.create_all()

    load_regions()
    load_affiliations()

    # Import data into database

    raw_poems = os.listdir('raw_poems/')


    for f in raw_poems:
        text = open('raw_poems/' + f)

        soup = BeautifulSoup(text, 'html.parser')

        
        author = load_author(soup)
        poem = load_poem(soup, author)
        subjects = load_subjects(soup, poem)
        db.session.commit()

        text.close()