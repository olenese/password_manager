from collections import UserDict
from distutils.dep_util import newer_pairwise
from email.generator import Generator
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user, user_logged_in
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
    userlogins = Logins.query.filter_by(userID=current_user.id).all()
    print(userlogins)
    # Creates a list to store the logins from the database.
    new_login_list = []
    for i in userlogins:
        # Adds the logins to a new list with the decrypted password to make the user able to see their password.
        decrypted_login = Logins(id=i.id, location=i.location, username=i.username, password=decrypt(i.password), url=i.url, note=i.note, userID=current_user.id)
        print(decrypted_login)
        # Appends the new list to the new_login_list list for each login. 
        new_login_list.append(decrypted_login)
    for i in new_login_list:
        print(i.location)

    return render_template('editpassword.html', website=new_login_list)

@editpassword.route('/editpassword', methods=['POST'])
@login_required
def changepassword_post():

    editpasswordlocation = request.form.get('location')
    newpassword = request.form.get('newpassword')


    postnewpassword = Users(userID=current_user.id, location=editpasswordlocation, password=encrypt(newpassword))
    db.session.update(postnewpassword)
    db.session.commit()

    return render_template('editpassword.html' )

    userlogins = Logins.query.filter_by(userID=current_user.id).all()
    # Creates a list to store the logins from the database.
    new_login_list = []
    for i in userlogins:
        # Adds the logins to a new list with the decrypted password to make the user able to see their password.
        decrypted_login = Logins(id=i.id, location=i.location, username=i.username, password=decrypt(i.password), url=i.url, note=i.note, userID=current_user.id)
        # Appends the new list to the new_login_list list for each login. 
        new_login_list.append(decrypted_login)
    # Sends the new_login_list list to the viewlogins.html page to be displayed.