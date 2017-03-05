from model import db, connect_to_db, Role, Organization
from server import app

connect_to_db(app)
db.drop_all()
db.create_all()

for name in ['superadmin', 'admin', 'donor', 'edit']:
    role = Role(name)
    db.session.add(role)

for i in range(3):
    organization = Organization(
        'The Lillith Fund {}'.format(i + 1),
        "The Lillith Fund {} helps people pay for an abortion when they can't afford it.".format(i + 1),
        'http://lillithfund.org/',
        'info@lillithfund.org',
        None
    )
    organization.address = 'P.O. Box 759, Anytown, USA, 93856'
    organization.template_hero_image = open('hero.jpg', 'rb').read()
    db.session.add(organization)

db.session.commit()

print "DB created."