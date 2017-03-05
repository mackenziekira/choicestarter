from model import db, connect_to_db, Role, Organization
from server import app

connect_to_db(app)
db.drop_all()
db.create_all()

for name in ['superadmin', 'admin', 'donor', 'edit']:
    role = Role(name)
    db.session.add(role)

organization = Organization(
    'South Kentucky Abortion Fund',
    'Providing financial support for abortion access since 1994.',
    'http://skyaa.org/',
    'support@skyaa.org',
    None
)
organization.address = '68 Choice Road, PO Box 541, Monticello, KY 42633'
organization.template_featured = 1
organization.template_hero_image = open('org-1.jpg', 'rb').read()
db.session.add(organization)
organization = Organization(
    'Central Region Access Coalition',
    'Helping people throughout the central region access abortions.',
    'http://crac.org/',
    'hello@crac.org',
    None
)
organization.address = '154 Western Ave, PO Box 67, Red Barrel, WY 78463'
organization.template_featured = 2
organization.template_hero_image = open('org-2.jpg', 'rb').read()
db.session.add(organization)
organization = Organization(
    'Far Western Abortion Access Fund',
    'Ensuring abortion support for all people in the Far Western region.',
    'http://fwaaf.org/',
    'fwaaf@fwaaf.org',
    None
)
organization.address = '98 Maple Drive, PO Box 899, Palm Break, CO 09839'
organization.template_featured = 3
organization.template_hero_image = open('org-3.jpg', 'rb').read()
db.session.add(organization)

db.session.commit()

print "DB created."