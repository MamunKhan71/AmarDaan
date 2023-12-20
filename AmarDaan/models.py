from amardaan import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    profile_picture = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    campaigns = db.relationship('Campaign', backref='user_campaigns', lazy=True)
    transactions = db.relationship('Transactions', backref='user_transactions', lazy=True)


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camp_owner = db.Column(db.String(200))
    camp_name = db.Column(db.String(200))
    camp_sub_name = db.Column(db.String(200))
    camp_category = db.Column(db.String(200))
    CATEGORY_CHOICES = {
        "18": "Animals & Pets",
        "19": "Business & Startups",
        "20": "Causes & Charities",
        "8": "Community",
        "21": "Creative",
        "22": "Education & Learning",
        "7": "Family",
        "23": "Funerals & Tributes",
        "62": "Legal",
        "25": "Medical & Healing",
        "28": "Other Funding",
        "6": "Personal",
        "29": "Religious",
        "30": "Special Events",
        "31": "Sports",
        "33": "Volunteer & Travel",
        "35": "Weddings & Honeymoon",
    }
    # Add this field to store the category name
    camp_category_name = db.Column(db.String(100))
    camp_division = db.Column(db.String(200))
    camp_zilla = db.Column(db.String(200))
    camp_upzilla = db.Column(db.String(200))
    camp_payment = db.Column(db.String(200))
    camp_mobile = db.Column(db.String(200))
    camp_deadline = db.Column(db.DateTime(timezone=True))
    camp_story = db.Column(db.String(200))
    camp_photo = db.Column(db.String(200))
    camp_gender = db.Column(db.String(200))
    camp_age = db.Column(db.String(200))
    camp_occupation = db.Column(db.String(200))
    camp_goal = db.Column(db.Integer)
    camp_video = db.Column(db.String(200))
    camp_social = db.Column(db.String(200))
    camp_aboutus = db.Column(db.String(200))
    camp_status = db.Column(db.String(20))  # Add this field
    camp_fund_raised = db.Column(db.Integer)  # Add this field
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Campaign_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer)
    camp_name = db.Column(db.String(100))
    camp_status = db.Column(db.String(20))
    camp_actions = db.Column(db.String(20))



class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(200))
    donation_amount = db.Column(db.Integer)
    hide_amount = db.Column(db.Integer)
    hide_comments = db.Column(db.Integer)
    hide_name = db.Column(db.Integer)
    follower = db.Column(db.Integer)
    donation_comment = db.Column(db.String(200))
    transaction_date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(200))
    method = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
