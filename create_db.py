from model import db, connect_to_db, Role
from server import app

connect_to_db(app)
db.drop_all()
db.create_all()

for name in ['superadmin', 'admin', 'donor', 'edit']:
	role = Role(name)
	db.session.add(role)

db.session.commit()


print "DB created."