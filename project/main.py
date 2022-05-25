from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, url_for, request, flash
from . import db
from .generatorbackend import randomcharacter, passhpraseEN, generatePIN
from .checkhavibeenpwnd import getpass



main = Blueprint('main', __name__)

# Creates the landing page for new users and what shows when they log in
@main.route('/')
def index():
    return render_template('index.html')

# Creates the profile page for users, the users are required to be logged in to view this page
@main.route('/profile')
@login_required
def profile():

    output = getpass(current_user.id)
    print(output)
    if output != None:
        print(output)
        return render_template('profile.html', name=current_user.name, email=current_user.email, id=output)
    else:
        print("nothing here")
        return render_template('profile.html', name=current_user.name)


# Creates the page for the users to add a login to their vault, the users are required to be logged in to view this page

