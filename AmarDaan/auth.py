import random

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        passw = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, passw):
                flash("Account Logged Successfully!", category='success')
                login_user(user=user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password!", category='error')

        return redirect(url_for('views.home'))
    return render_template('user_form.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/forgot_password')
def forgot_password():

    return render_template('forgot_password.html', user=current_user)

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        passw = request.form.get('password')
        print(f"{fname} --  {lname}")
        user = User.query.filter_by(email=email).first()

        if user:
            flash('User Already Exists! Please Login', category='error')
            print(email)
        else:
            new_user = User(
                first_name=fname,
                last_name=lname,
                username=f"{fname} {lname}",
                email=email,
                password=generate_password_hash(password=passw, method='sha256'),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Successfully!", category='success')
            login_user(user=new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('user_form.html', user=current_user)

