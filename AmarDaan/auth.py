from flask import Blueprint , render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('user_form.html')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/signup')
def signup():
    return "<p>Sign Up</p>"