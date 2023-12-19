import datetime

from flask import jsonify, Blueprint, render_template, request, current_app, redirect, url_for, session, flash
from flask_login import login_required, current_user
from .models import Campaign, Campaign_Category
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from werkzeug.utils import secure_filename

from sslcommerz_lib import SSLCOMMERZ
import os
import time
import smtplib
from email.mime.text import MIMEText
import random
import requests
import json

SSLCZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'
import uuid
from werkzeug.local import LocalProxy

views = Blueprint('views', __name__)


@views.route('/')
def home():
    campaigns = Campaign.query.all()
    return render_template('index.html', user=current_user, campaign=campaigns)


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
    return render_template('statistics.html', user=user, campaigns=user_campaigns)


@views.route('/campaign', methods=["GET", "POST"])
def campaign():
    user = current_user if current_user.is_authenticated else None
    if user is None:
        return render_template('campaign_list.html', user=None)
    else:
        if request.method == "POST":
            camp_name = request.form.get('camp_name')
            camp_sub_name = request.form.get('camp_sub_name')
            camp_category = request.form.get('camp_category')
            camp_division = request.form.get('camp_division')
            camp_zilla = request.form.get('camp_zilla')
            camp_upzilla = request.form.get('camp_upzilla')
            camp_payment = request.form.get('camp_payment')
            camp_mobile = request.form.get('camp_mobile')
            camp_deadline = datetime.datetime.strptime(request.form.get('camp_deadline'), '%Y-%m-%d')
            camp_story = request.form.get('camp_story')
            photo = request.files['camp_photo']
            if photo.filename == '':
                return 'No selected file'
            else:
                upload_folder = os.path.join(current_app.root_path, 'static', current_app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_folder, exist_ok=True)
                filename = secure_filename(photo.filename)
                relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace(os.path.sep, '/')
                full_path = os.path.join(upload_folder, filename)
                photo.save(full_path)

            print("Relative Path:", relative_path)
            print("Full Path:", full_path)

            camp_gender = request.form.get('camp_gender')
            camp_age = request.form.get('camp_age')
            camp_occupation = request.form.get('camp_occupation')
            camp_goal = request.form.get('camp_goal')
            camp_video = request.form.get('camp_video')
            camp_social = request.form.get('camp_social')
            camp_aboutus = request.form.get('camp_aboutus')
            camp_owner = current_user.name
            new_campaign = Campaign(
                camp_name=camp_name,
                camp_sub_name=camp_sub_name,
                camp_category=camp_category,
                camp_division=camp_division,
                camp_zilla=camp_zilla,
                camp_upzilla=camp_upzilla,
                camp_payment=camp_payment,
                camp_mobile=camp_mobile,
                camp_deadline=camp_deadline,
                camp_owner=camp_owner,
                camp_story=camp_story,
                camp_photo=relative_path,  # Saving the file path in the database
                camp_gender=camp_gender,
                camp_age=camp_age,
                camp_occupation=camp_occupation,
                camp_goal=camp_goal,
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

    return redirect(url_for('views.user_profile'))


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
            print(email)
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


@views.route('/profile')
def profile():
    return render_template('user_profile.html', user=current_user)


@views.route('/campaign_details', methods=["GET", "POST"])
def campaign_details():
    campaign_id = request.form.get('campaign_id')

    # Query the database to retrieve the campaign based on the campaign_id
    campaigns = Campaign.query.filter_by(id=campaign_id).first()

    # Check if the campaign exists
    if campaigns:
        # Process the donation or redirect to a donation page
        # For now, let's redirect to the campaign details page
        return render_template('campaign_details.html', user=current_user, campaign=campaigns)
    else:
        # Handle the case where the campaign is not found
        return render_template('error.html')

    return render_template('campaign_details.html', user=current_user)


@views.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    send_email(subject=subject, body=message, sender="amardaan247@gmail.com", recipients=email,
               password="ecaflcbwzegogtnr", name=name)
    return render_template("payment_success.html")


@views.route('/faq')
def faq():
    return render_template('faq.html', user=current_user)


@views.route('/campaign_list')
def campaign_list():
    return render_template('campaign_list.html', user=current_user)


def get_session(name, amount):
    post_data = {
        "store_id": "amard65277e36db8a5",
        "store_passwd": "amard65277e36db8a5@ssl",
        "total_amount": 500,
        "currency": "BDT",
        "tran_id": uuid.uuid4(),
        "success_url": "http://ssltest.com:5000/success",
        "fail_url": "http://ssltest.com:5000/fail",
        "cancel_url": "http://ssltest.com:5000/cancel",
        "ipn_url": "http://ssltest.com:5000/ipn",
        "cus_name": "Md. Mamun",
        "cus_email": "cust@yahoo.com",
        "cus_add1": "Dhaka",
        "cus_add2": "Dhaka",
        "cus_city": "Dhaka",
        "cus_state": "Dhaka",
        "cus_postcode": "1000",
        "cus_country": "Bangladesh",
        "cus_phone": "01711111111",
        "cus_fax": "01711111111",
        "ship_name": "Customer Name",
        "ship_add1": "Dhaka",
        "ship_add2": "Dhaka",
        "ship_city": "Dhaka",
        "ship_state": "Dhaka",
        "ship_postcode": "1000",
        "ship_country": "Bangladesh",
        "multi_card_name": "mastercard,visacard,amexcard",
        "value_a": "ref001_A",
        "value_b": "ref002_B",
        "value_c": "ref003_C",
        "value_d": "ref004_D",
        "shipping_method": "YES",
        "product_name": "credit",
        "product_category": "general",
        "product_profile": "general"
    }

    response = requests.post(SSLCZ_SESSION_API, post_data)

    return (response.json()["sessionkey"], response.json()["GatewayPageURL"])


@views.route('/get-ssl-session', methods=['POST', 'GET'])
def get_ssl_session():
    campaign_id = request.form.get('campaign_id')
    campaign = Campaign.query.get(campaign_id)

    if campaign:
        name = "Mamun"  # Replace with the actual name
        amount = int(request.form.get('donation_amount', 0))  # Assuming the form field is named 'donation_amount'
        session, gateway = get_session(name, amount)

        # Redirect to the payment gateway
        return redirect(gateway)

    # Redirect to an error page or handle the case where the campaign is not found
    return render_template('error.html', user=current_user)

# Your other routes and code here



@views.route('/success', methods=['POST', 'GET'])
def success():
    response = request.form.to_dict()
    # process your data store it or do anything you prefer

    return render_template('payment_success.html', user=current_user);


@views.route('/fail', methods=['POST'])
def fail():
    response = request.form.to_dict()

    return redirect('http://localhost:80/fail');


@views.route('/cancel', methods=['POST'])
def cancel():
    response = request.form.to_dict()

    return redirect('http://localhost:80/cancel')


@views.route('/donation_page/<id>', methods=["POST", "GET"])
def donation_page(id):
    if request.method == "POST":
        campaign_id = request.form.get('campaignId')
        print(campaign_id)
        # Process the donation and campaign_id as needed

    # Retrieve the campaign information for the GET request
    campaign = Campaign.query.filter_by(id=id).first()

    return render_template('donation_page.html', user=current_user, campaign=campaign)



@views.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html', user=current_user)


@views.route('/subscribe_newsletter', methods=["POST"])
def subscribe_newsletter():
    email = request.form.get('email')
    message = f'Congratulations!\n\nYou have subscribe to the weekly newsletter!\n\nRegards,\n\nTeam AmarDaan'
    send_email(subject="Subscriptions Successful!", body=message, sender='amardaan247@gmail.com', recipients=email,
               password='ecaflcbwzegogtnr')
    print("returned!")
    return render_template('index.html', user=current_user)


@views.route('/about_us', methods=["GET"])
def about_us():
    return render_template('about_us.html', user=current_user)


@views.route('/add_campaign', methods=["GET", "POST"])
def add_campaign():
    campaigns = Campaign_Category.query.all()
    return render_template('add_campaign.html', user=current_user, campaigns=campaigns)


@views.route('/add_new_campaign', methods=["GET", "POST"])
def add_new_campaign():
    if request.method == 'POST':
        camp_id = request.form['camp_id']
        camp_name = request.form['camp_name']
        camp_status = request.form['camp_status']
        camp_action = request.form['camp_actions']

        new_campaign = Campaign_Category(camp_id=camp_id, camp_name=camp_name, camp_status=camp_status,
                                         camp_actions=camp_action)

        db.session.add(new_campaign)
        db.session.commit()

    # Fetch all campaign categories after adding a new one
    campaigns = Campaign_Category.query.all()

    return render_template('add_new_campaign.html', user=current_user)


@views.route('/delete_campaign/<int:campaign_id>', methods=['POST', 'GET'])
def delete_campaign(campaign_id):
    # Fetch the campaign from the database using campaign_id
    campaign = Campaign_Category.query.get(campaign_id)

    # Delete the campaign from the database
    db.session.delete(campaign)
    db.session.commit()

    flash('Campaign deleted successfully!', 'success')

    # Redirect to the campaign list page or another appropriate page
    return redirect(url_for('views.add_campaign'))


@views.route('/edit_campaigns', methods=["GET", "POST"])
def edit_campaigns():
    campaigns = Campaign.query.all()

    # Debugging: Print the campaigns to check if data is fetched
    print("Campaigns:", campaigns)

    return render_template('edit_campaigns.html', user=current_user, campaigns=campaigns)

@views.route('/delete_campaigns/<int:campaign_id>', methods=['POST', 'GET'])
def delete_campaigns(campaign_id):
    # Fetch the campaign from the database using campaign_id
    campaign = Campaign.query.get(campaign_id)

    if not campaign:
        flash('Campaign not found!', 'danger')
        return redirect(url_for('views.edit_campaigns'))

    try:
        # Delete the campaign from the database
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign deleted successfully!', 'success')
    except Exception as e:
        print("Error:", str(e))
        db.session.rollback()
        flash('Error deleting campaign!', 'danger')

    # Redirect to the edit_campaigns page or another appropriate page
    return redirect(url_for('views.edit_campaigns'))


@views.route('/transactions', methods=["GET", "POST"])
def transactions():
    return render_template('transactions.html', user=current_user)