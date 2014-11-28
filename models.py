from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from secrets import db

'''
Database Connection via SQLAlchemy
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@localhost/watching'.format(db['username'], db['password'])
db = SQLAlchemy(app)