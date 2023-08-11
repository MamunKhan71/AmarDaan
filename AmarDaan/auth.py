from flask import Blueprint , render_template , request , flash , redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        passw = request.form.get('password')
        
        user = User.query.filter_by(email).first()
        if user:
            if check_password_hash(user.password, passw):
                print('Login Successful!')
            else:
                print('Login Field')


        return redirect(url_for('views.home'))
    return render_template('user_form.html')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        passw = request.form.get('password')
        
        if len(email) < 15:
            flash('Email must be greater than 4', category='error')
            print(email)
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password=passw, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Succesfully!", category='success')
            return redirect(url_for('views.home'))
    return render_template('user_form.html')