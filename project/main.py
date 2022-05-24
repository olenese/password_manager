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
    getpass()
    return render_template('profile.html', name=current_user.name)


# Creates the page for the users to add a login to their vault, the users are required to be logged in to view this page

# GET route for adding a new login, used during navigation (in the page header)
@main.route('/newlogin')
@login_required
def newlogin():
    return render_template('newlogin.html', name=current_user.name)
