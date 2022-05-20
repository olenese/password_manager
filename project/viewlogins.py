from collections import UserDict
from distutils.dep_util import newer_pairwise
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Logins, Users
from .security import encrypt, decrypt
from . import db

# Creates the blueprint for the viewlogins page
viewlogins = Blueprint('viewlogins', __name__)


# Creates the viewlogins page for users, the users are required to be logged in to view this page
@viewlogins.route('/viewlogins')
@login_required
def viewlogin():
    # Fetch the amount of logins the user has based on their userID in the database. 
    userlogins = Logins.query.filter_by(userID=current_user.id).all()
    # Creates a list to store the logins from the database.
    new_login_list = []
    for i in userlogins:
        # Adds the logins to a new list with the decrypted password to make the user able to see their password.
        decrypted_login = Logins(id=i.id, location=i.location, username=i.username, password=decrypt(i.password), url=i.url, note=i.note, userID=current_user.id)
        # Appends the new list to the new_login_list list for each login. 
        new_login_list.append(decrypted_login)
    # Sends the new_login_list list to the viewlogins.html page to be displayed.
    return render_template('viewlogins.html',name = current_user.name, logins=new_login_list)

