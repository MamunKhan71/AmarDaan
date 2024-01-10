import random
import smtplib
from email.mime.text import MIMEText

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, ProfileSettings
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


def send_email(subject, body, sender, recipients, password, name=None):
    if name != None:
        f_msg = f"Message From : {name} \n{body}"
        msg = MIMEText(f_msg)
    else:
        msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message Sent!")


def otp_verification(name, email):
    otp = random.randint(pow(10, 5), (pow(10, 6) - 1))
    subject = "Your OTP Verification Code"
    body = f"Dear {name},\n\nThank you for choosing AmarDaan! To ensure the security of your account, we have sent you a One-Time Password (OTP) for verification purposes. \n\nYour OTP: {otp} \n\nPlease enter this OTP on the verification page to complete the process. Please note that this OTP is valid for a limited time and should not be shared with anyone.\n\nIf you did not initiate this request or have any concerns, please contact our customer support immediately at Customer Support amardaan247@gmail.com. \n\nThank you for your trust in AmarDaan."
    sender = "amardaan247@gmail.com"
    recipients = email
    password = "ecaflcbwzegogtnr"
    send_email(subject, body, sender, recipients, password)
    return otp


@auth.context_processor
def inject_settings():
    settings = ProfileSettings.query.filter_by(id=1).first()

    # Return a dictionary with the variable you want to inject into the template context
    return {'settings': settings}


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

        # return redirect(url_for('views.home'))
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
        session['signup'] = request.form
        print(f"{fname} --  {lname}")
        user = User.query.filter_by(email=email).first()

        if user:
            flash('User Already Exists! Please Login', category='error')
            print(email)
        else:
            otp = otp_verification(fname, email)
            session['auth_generated_otp'] = otp
            return render_template('otp_page.html', email=email, otp=otp, update_profile=False)

    return render_template('user_form.html', user=current_user)


@auth.route('/auth_otp', methods=['POST', "GET"])
def auth_otp():
    user_otp = f"{request.form.get('first')}{request.form.get('second')}{request.form.get('third')}{request.form.get('fourth')}{request.form.get('fifth')}{request.form.get('sixth')}"
    generated_otp = session.get('auth_generated_otp')
    form_datas = session.get('signup', {})

    if user_otp == str(generated_otp):
        try:
            print("success")
            new_user = User(
                first_name=form_datas.get('firstname'),
                last_name=form_datas.get('lastname'),
                username=f"{form_datas.get('firstname')} {form_datas.get('lastname')}",
                email=form_datas.get('email'),
                password=generate_password_hash(password=form_datas.get('password'), method='sha256'),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Successfully!", category='success')
            login_user(user=new_user, remember=True)
            return redirect(url_for('views.home'))
        except Exception as e:
            print("Error:", str(e))
    else:
        return render_template('wrong_otp.html', message="Invalid OTP.")
