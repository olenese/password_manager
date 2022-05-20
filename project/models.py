from flask_login import UserMixin
from sqlalchemy import ForeignKey
from . import db

# Create a Users model with the following attributes to make python able to query the database for the user authentication.

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# Create a Logins model with the following attributes to make python able to query the database for the logins information.

class Logins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))
    url = db.Column(db.String(255))
    note = db.Column(db.String(1000))
    userID = db.Column(db.Integer, ForeignKey('users.id'))

