from model import db, connect_to_db
from server import app

connect_to_db(app)
db.drop_all()
db.create_all()

print "DB created."