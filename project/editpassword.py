from collections import UserDict
from distutils.dep_util import newer_pairwise
from email.generator import Generator
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Logins, Users
from .security import encrypt, decrypt
from .generatorbackend import randomcharacter
from . import db



# Creates the blueprint for the viewlogins page
editpassword = Blueprint('editpassword', __name__)


# Creates the viewlogins page for users, the users are required to be logged in to view this page
@editpassword.route('/editpassword')
@login_required
def changepassword():
    return render_template('editpassword.html')

@editpassword.route('/editpassword', methods=['POST'])
@login_required
def changepassword_post():
    return render_template('editpassword.html')

