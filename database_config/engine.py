import sqlalchemy
import os

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
port = os.getenv("DB_PORT")

engine = sqlalchemy.create_engine('postgresql://{}:{}@localhost:{}/postgres'
    .format(user, password, port))