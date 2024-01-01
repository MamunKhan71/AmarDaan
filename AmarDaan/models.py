from datetime import datetime

from amardaan import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(150), unique=True)
    phone_number = db.Column(db.String(20))
    country = db.Column(db.String(50))
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    other = db.Column(db.String(150))
    password = db.Column(db.String(150))
    profile_picture = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    campaigns = db.relationship('Campaign', backref='user_campaigns', lazy=True)
    transactions = db.relationship('Transactions', backref='user_transactions', lazy=True)


class Campaign_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer)
    camp_name = db.Column(db.String(100))
    camp_status = db.Column(db.String(20))

    # ForeignKey to establish a relationship with the Campaign model
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))

    # Relationship definition (optional, depending on your use case)
    campaign = db.relationship('Campaign', backref='campaign_categories', lazy=True)


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_approve = db.Column(db.Integer)
    camp_owner = db.Column(db.String(200))
    camp_name = db.Column(db.String(200))
    camp_sub_name = db.Column(db.String(200))
    camp_category = db.Column(db.String(200))
    CATEGORY_CHOICES = {}

    @classmethod
    def update_category_choices(cls):

        categories = Campaign_Category.query.all()
        cls.CATEGORY_CHOICES = {str(category.camp_id): category.camp_name for category in categories}

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


class Inbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"Inbox(id={self.id}, name={self.name}, subject={self.subject}, message={self.message} status={self.status}, created_on={self.created_on})"


class ProfileSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(255), nullable=False)
    website_text = db.Column(db.String(255), nullable=False)
    about = db.Column(db.String(255), nullable=False)