from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Campaign
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
import time
import smtplib
from email.mime.text import MIMEText
import random
views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@views.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard():
    user = current_user
    print(user.profile_picture)
    user_campaigns = Campaign.query.filter_by(user_id=user.id).all()
    if request.method == "POST":
        note = request.form.get('note')
        new_note = Campaign(camp_name=note, user_id=current_user.id)  # Assuming camp_name is the correct attribute
        db.session.add(new_note)
        db.session.commit()
        print("Note added successfully!")
    return render_template('dashboard.html', user=user, campaigns=user_campaigns)

@views.route('/campaign', methods=["GET", "POST"])
def campaign():
    user = current_user if current_user.is_authenticated else None
    if user is None:
        return render_template('campaign_list.html', user=None)
    else:
        if request.method == "POST":
            camp_name = request.form.get('camp_name')
            camp_category = request.form.get('camp_category')
            camp_division = request.form.get('camp_division')
            camp_zilla = request.form.get('camp_zilla')
            camp_upzilla = request.form.get('camp_upzilla')
            camp_payment = request.form.get('camp_payment')
            camp_mobile = request.form.get('camp_mobile')
            camp_deadline = request.form.get('camp_deadline')
            camp_story = request.form.get('camp_story')
            photo = request.files['camp_photo']
            if photo.filename == '':
                return 'No selected file'
            else:
                upload_folder = os.path.join(current_app.root_path, 'static', current_app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_folder, exist_ok=True)
                filename = os.path.join(upload_folder, photo.filename)
                photo.save(filename)      

            camp_gender = request.form.get('camp_gender')
            camp_age = request.form.get('camp_age')
            camp_occupation = request.form.get('camp_occupation')
            camp_video = request.form.get('camp_video')
            camp_social = request.form.get('camp_social')
            camp_aboutus = request.form.get('camp_aboutus')

            new_campaign = Campaign(
                camp_name=camp_name,
                camp_category=camp_category,
                camp_division=camp_division,
                camp_zilla=camp_zilla,
                camp_upzilla=camp_upzilla,
                camp_payment=camp_payment,
                camp_mobile=camp_mobile,
                camp_deadline=camp_deadline,
                camp_story=camp_story,
                camp_photo=filename,  # Saving the file path in the database
                camp_gender=camp_gender,
                camp_age=camp_age,
                camp_occupation=camp_occupation,
                camp_video=camp_video,
                camp_social=camp_social,
                camp_aboutus=camp_aboutus,
                user_id=current_user.id,
            )
            db.session.add(new_campaign)
            db.session.commit()
            print("Data Saved Successfully!")

    return render_template('campaign.html', user=user)

@views.route('/upload_profile_picture', methods=["POST"])
@login_required
def upload_profile_picture():
    if request.method == "POST":
        user = current_user
        profile_picture = request.files['profile_picture']
        if profile_picture.filename == '':
            return 'No selected file'
        else:
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)  # Create the directory if it doesn't exist
            filename = os.path.join(upload_folder, profile_picture.filename)
            profile_picture.save(filename)

        print("Uploaded File:", filename)  # Debug print

        # Update user's profile_picture attribute with the relative path to the uploaded image
        relative_path = os.path.relpath(filename, os.path.join(current_app.root_path, 'static'))
        user.profile_picture = relative_path
        user.profile_picture_updated = time.time()  # Set to the current timestamp
        db.session.commit()
        
        print("Profile Picture Updated Successfully!")

    return redirect(url_for('views.dashboard'))

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message Sent!")

def otp_verification():
    otp = random.randint(pow(10, 5), (pow(10, 6) - 1))
    subject = "Your OTP Verification Code"
    body = f"Dear {current_user.name},\n\nThank you for choosing AmarDaan! To ensure the security of your account, we have sent you a One-Time Password (OTP) for verification purposes. \n\nYour OTP: {otp} \n\nPlease enter this OTP on the verification page to complete the process. Please note that this OTP is valid for a limited time and should not be shared with anyone.\n\nIf you did not initiate this request or have any concerns, please contact our customer support immediately at Customer Support amardaan247@gmail.com. \n\nThank you for your trust in AmarDaan."
    sender = "amardaan247@gmail.com"
    recipients = current_user.email
    password = "ecaflcbwzegogtnr"
    send_email(subject, body, sender, recipients, password)
    return otp

@views.route('/update_profile', methods=["POST"])
@login_required
def update_profile():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    email = request.form.get('email')
    facebook = request.form.get('facebook')
    instagram = request.form.get('instagram')
    updated_name = f"{first_name} {last_name}"

    # Generate and store OTP
    generated_otp = otp_verification()
    session['generated_otp'] = generated_otp

    return render_template('otp_page.html', user=current_user, otp=generated_otp)


@views.route('/otp_verified', methods=['POST'])
@login_required
def otp_verified():
    user_otp = f"{request.form.get('first')}{request.form.get('second')}{request.form.get('third')}{request.form.get('fourth')}{request.form.get('fifth')}{request.form.get('sixth')}"
    generated_otp = session.get('generated_otp')

    if user_otp == generated_otp:
        try:
            user = current_user

            # Retrieve updated_name, email, etc. from the form
            updated_name = f"{request.form.get('first_name')} {request.form.get('last_name')}"
            email = request.form.get('email')
            password = request.form.get('password')
            facebook = request.form.get('facebook')
            instagram = request.form.get('instagram')

            if updated_name:
                user.name = updated_name
            if email:
                user.email = email
            if password:
                user.password = generate_password_hash(password=password, method='sha256')
            if facebook:    
                user.facebook = f"https://www.fb.com/{facebook}"
            if instagram:
                user.instagram = f"https://www.instagram.com/{instagram}"

            db.session.commit()
            print("Profile Updated Successfully!")
        except Exception as e:
            print("Error:", str(e))
            db.session.rollback()
            return render_template('error.html', message="An error occurred while saving data.")
    else:
        return render_template("error.html", message="ERROR 404 - WRONG OTP")

@views.route('/statistics')
@login_required
def statistics():
    return render_template('statistics.html', user=current_user)
