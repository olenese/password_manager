from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, url_for, request, flash
from .models import Logins, Users
from .security import encrypt, decrypt
from . import db
from .generatorbackend import passphraseNO, randomcharacter, passhpraseEN
from .generatorbackend import randomcharacter
from .generatorbackend import passhpraseEN
from .generatorbackend import generatePIN

manager = Blueprint('manager', __name__)

# @manager.route('/newlogin', methods=['POST'])
# @login_required
# def generatepassword():
#     passwordtype = request.args.get('passwordselection')
#     if passwordtype == '1':
#         generatedpassword = passhpraseEN(4)
#     elif passwordtype == '2':
#         generatedpassword = passphraseNO(4)
#     elif passwordtype == '3':
#         generatedpassword = randomcharacter(16)
#     else:
#         generatedpassword = request.form.get('password')
#     return render_template('newlogin.html', password=generatedpassword)

@manager.route('/newlogin', methods=['POST'])
@login_required
def newlogin_post():
    if ('action' in request.form and request.form['action'] == 'Generate a password'):
        password_length = safe_cast(request.form['password_length'], int)
        password_type = request.form['password_type']

        # TODO: need to validate that the password_length is within acceptable range for the password type, perhaps add an error section to the new login page

        match safe_cast(password_type, int):
            case 1:
                return render_template(
                    'newlogin.html',
                    name = current_user.name,
                    password = randomcharacter(password_length),
                    password_length = password_length,
                    password_type = password_type,
                    password_min = 16,
                    password_max = 64
                )
            case 2:
                return render_template(
                    'newlogin.html',
                    name = current_user.name,
                    password = passhpraseEN(password_length),
                    password_length = password_length,
                    password_type = password_type,
                    password_min = 2,
                    password_max = 6
                )
            case 3:
                return render_template(
                    'newlogin.html',
                    name = current_user.name,
                    password = generatePIN(password_length),
                    password_length = password_length,
                    password_type = password_type,
                    password_min = 4,
                    password_max = 24
                )
    else:
        location = request.form.get('location')
        username = request.form.get('username')
        finishedpassword = request.form.get('password')
        url = request.form.get('url')
        note = request.form.get('note')
        new_login = Logins(location=location, username=username, password=encrypt(finishedpassword), url=url, note=note, userID=current_user.id)
        db.session.add(new_login)
        db.session.commit()
        return redirect(url_for('main.profile'))

def safe_cast(val, type, default=None):
    try:
        return type(val)
    except ValueError:
        return default
