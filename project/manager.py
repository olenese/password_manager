from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, url_for, request, flash
from .models import Logins, Users
from .security import encrypt, decrypt
from . import db
from .generatorbackend import passphraseNO, randomcharacter, passhpraseEN

manager = Blueprint('manager', __name__)

@manager.route('/newlogin', methods=['POST'])
@login_required
def generatepassword():
    passwordtype = request.args.get('passwordselection')
    if passwordtype == '1':
        generatedpassword = passhpraseEN(4)
    elif passwordtype == '2':
        generatedpassword = passphraseNO(4)
    elif passwordtype == '3':
        generatedpassword = randomcharacter(16)
    else:
        generatedpassword = request.form.get('password')
    return render_template('newlogin.html', password=generatedpassword)

@manager.route('/newlogin', methods=['POST'])
@login_required
def newlogin_post():
    location = request.form.get('location')
    username = request.form.get('username')
    finishedpassword = request.form.get('password')
    url = request.form.get('url')
    note = request.form.get('note')
    new_login = Logins(location=location, username=username, password=encrypt(finishedpassword), url=url, note=note, userID=current_user.id)
    db.session.add(new_login)
    db.session.commit()
    return redirect(url_for('main.profile'))

