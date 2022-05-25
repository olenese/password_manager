from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, url_for, request, flash
from .models import Logins, Users
from .security import encrypt, decrypt
from . import db
from .generatorbackend import randomcharacter, passhpraseEN, generatePIN

manager = Blueprint('manager', __name__)

def safe_cast(val, type, default = None):
    try:
        return type(val) or default
    except:
        return default

def is_generate_password_action(request):
    return 'action' in request.form and request.form['action'] == 'Generate a password'

class LoginViewModel():
    is_editing = False
    password_length = None
    password_type = None
    password_min = None
    password_max = None
    id = None
    website = ''
    username = ''
    password = ''
    url = ''
    note = ''

    def __init__(self, form, login = None):
        # TODO: need to validate that the password_length is within acceptable range for the password type, perhaps add an error section to the new login page
        self.password_length = safe_cast(form.get('password_length'), int, 16)
        self.password_type = safe_cast(form.get('password_type'), int, 1)
        self.password_min = safe_cast(form.get('password_min'), int, 16)
        self.password_max = safe_cast(form.get('password_max'), int, 64)

        if login:
            self.is_editing = True
            self.id = login.id
            self.website = login.location
            self.username = login.username
            self.password = decrypt(login.password)
            self.url = login.url
            self.note = login.note
        else:
            self.website = form.get('website') or ''
            self.username = form.get('username') or ''
            self.finishedpassword = form.get('password') or ''
            self.url = form.get('url') or ''
            self.note = form.get('note') or ''

    def generate_password(self):
        match self.password_type:
            case 1:
                self.password = randomcharacter(self.password_length)
            case 2:
                self.password = passhpraseEN(self.password_length)
            case 3:
                self.password = generatePIN(self.password_length)

    def render(self):
        return render_template(
            'newlogin.html',
            id = self.id,
            name = current_user.name,
            website = self.website,
            username = self.username,
            password = self.password,
            url = self.url,
            note = self.note,
            is_editing = self.is_editing,
            password_length = self.password_length,
            password_type = self.password_type,
            password_min = self.password_min,
            password_max = self.password_max
        )

# @manager.route('/newlogin', methods=['POST'])
# @login_required
# def generatepassword():
#     passwordtype = request.args.get('passwordselection')
#     if passwordtype == '1':
#         gene
# ratedpassword = passhpraseEN(4)
#     elif passwordtype == '2':
#         generatedpassword = passphraseNO(4)
#     elif passwordtype == '3':
#         generatedpassword = randomcharacter(16)
#     else:
#         generatedpassword = request.form.get('password')
#     return render_template('newlogin.html', password=generatedpassword)

# GET route for adding a new login, used during navigation (in the page header)
@manager.route('/newlogin')
@login_required
def newlogin():
        view_model = LoginViewModel(request.form)

        return view_model.render()

@manager.route('/newlogin', methods=['POST'])
@login_required
def create_login():
    if (is_generate_password_action(request)):
        view_model = LoginViewModel(request.form)

        view_model.generate_password()

        return view_model.render()
    else:
        location = request.form.get('website')
        username = request.form.get('username')
        finishedpassword = request.form.get('password')
        url = request.form.get('url')
        note = request.form.get('note')
        new_login = Logins(location=location, username=username, password=encrypt(finishedpassword), url=url, note=note, userID=current_user.id)
        db.session.add(new_login)
        db.session.commit()
        return redirect(url_for('viewlogins.viewlogin'))

@manager.route('/edit-login/<id>', methods=['POST'])
@login_required
def update_login(id):
    id = safe_cast(id, int)

    if (is_generate_password_action(request)):
        view_model = LoginViewModel(request.form)

        view_model.id = id
        view_model.is_editing = True
        view_model.generate_password()

        return view_model.render()
    else:
        db.session.query(Logins).filter(Logins.id == id).update({
            Logins.location: request.form.get('website'),
            Logins.username: request.form.get('username'),
            Logins.password: encrypt(request.form.get('password')),
            Logins.url: request.form.get('url'),
            Logins.note: request.form.get('note')
        })
        db.session.commit()

        return redirect(url_for('viewlogins.viewlogin'))

@manager.route('/edit-login/<id>')
@login_required
def edit_login(id):
    id = safe_cast(id, int)
    login = Logins.query.filter_by(id=id).first()
    view_model = LoginViewModel(request.form, login)

    return view_model.render()
