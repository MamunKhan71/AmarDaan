from flask import Blueprint , render_template, request
from flask_login import login_required, logout_user, current_user
from .models import Campaign
from . import db
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@views.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard():
    if request.method == "POST":
        note = request.form.get('note')
        new_note = Campaign(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        print("note added successfully!")

    return render_template('dashboard.html', user=current_user)

@views.route('/campaign', methods=["GET", "POST"])
def campaign():
    user = current_user if current_user.is_authenticated else None
    if user == None:
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
            # camp_photo = request.form.get('camp_photo')
            camp_gender = request.form.get('camp_gender')
            camp_age = request.form.get('camp_age')
            camp_occupation = request.form.get('camp_occupation')
            camp_video = request.form.get('camp_video')
            camp_social = request.form.get('camp_social')
            camp_aboutus = request.form.get('camp_aboutus')

            new_campaign = Campaign(
            camp_name = camp_name,
            camp_category = camp_category,
            camp_division = camp_division,
            camp_zilla = camp_zilla,
            camp_upzilla = camp_upzilla,
            camp_payment = camp_payment,
            camp_mobile = camp_mobile,    
            camp_deadline = camp_deadline,
            camp_story = camp_story,
            # camp_photo = request.form.get('camp_photo')
            camp_gender = camp_gender,
            camp_age = camp_age,
            camp_occupation = camp_occupation,
            camp_video = camp_video,
            camp_social = camp_social,
            camp_aboutus = camp_aboutus,
            )
            db.session.add(new_campaign)
            db.session.commit()
            print("Data Saved Successfully!")
            
    return render_template('campaign.html', user=user)
