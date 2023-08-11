from flask import Blueprint , render_template, request
from flask_login import login_required, logout_user, current_user
from .models import Note
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
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        print("note added successfully!")

    return render_template('dashboard.html', user=current_user)
