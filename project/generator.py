######DEPRECATED######
######DEPRECATED######
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
generator = Blueprint('generator', __name__)


# Creates the viewlogins page for users, the users are required to be logged in to view this page
@generator.route('/generator')
@login_required
def pwgenerator():
    return render_template('generator.html')

@generator.route('/generator', methods=['POST'])
@login_required
def pwgenerator_post():
    password = ''
    passwordtype = request.form.get('passwordselection')
    passwordlength = request.form.get('passwordlength')
    if passwordtype == 1:
        print("got here")
        passsss = type(randomcharacter(passwordlength))
        print(passsss)
        password=randomcharacter(passwordlength)

    
    print(password)
    
    return render_template('generator.html', password=password)

