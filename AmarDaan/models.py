from amardaan import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camp_name = db.Column(db.String(200))
    camp_category = db.Column(db.String(200))
    camp_division = db.Column(db.String(200))
    camp_zilla = db.Column(db.String(200))
    camp_upzilla = db.Column(db.String(200))
    camp_payment = db.Column(db.String(200))
    camp_mobile = db.Column(db.String(200))
    camp_deadline = db.Column(db.String(200))
    camp_story = db.Column(db.String(200))
    camp_photo = db.Column(db.String(200))
    camp_gender = db.Column(db.String(200))
    camp_age = db.Column(db.String(200))
    camp_occupation = db.Column(db.String(200))
    camp_video = db.Column(db.String(200))
    camp_social = db.Column(db.String(200))
    camp_aboutus = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    profile_picture = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    campaigns = db.relationship('Campaign', backref='user', lazy=True)


class Campaign_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer)
    camp_name = db.Column(db.String(100))
    camp_status = db.Column(db.String(20))
    camp_actions = db.Column(db.String(20))
