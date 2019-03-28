# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
import os

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///envreq.db'

DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_INSTANCE=os.getenv('DB_INSTANCE')

DB_URL= "mysql+pymysql://%s:%s@%s:%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_INSTANCE)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://envreq:envreq@localhost:3306/envreqdb'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.secret_key = "mysecretkey"

app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

Bootstrap(app)

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

migrate = Migrate(app,db)

admin = Admin(app, name="Admin Dashboard", template_mode='bootstrap3')