import os

DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' \
+ os.environ['RDS_USERNAME'] + ':' + os.environ['RDS_PASSWORD'] +'@' + os.environ['RDS_HOSTNAME'] + \
':' + os.environ['RDS_PORT'] + '/' + os.environ['RDS_DB_NAME']

# Local psql
# SQLALCHEMY_DATABASE_URI = "postgresql:///choicestarter"