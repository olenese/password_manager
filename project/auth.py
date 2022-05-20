from crypt import methods
from flask import Blueprint, redirect, render_template, url_for, request, flash
import bcrypt
from flask_login import login_user, login_required, logout_user
from .models import Users
from . import db
import re


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    salt = bcrypt.gensalt()
    user = Users.query.filter_by(email=email).first()
    if len(password) <= 16:
        flash('Password must be at least 16 characters long.')
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = Users(email=email, name=name, password=bcrypt.hashpw(password.encode('utf-8'), salt))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))