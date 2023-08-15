from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from .models import Campaign
from . import db
import os
import time

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
        user.profile_picture = "Hi"
        user.profile_picture_updated = time.time()  # Set to the current timestamp
        db.session.commit()
        
        print("Profile Picture Updated Successfully!")

    return redirect(url_for('views.dashboard'))






