from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "amardaan.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mamunapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(path.dirname(__file__), DB_NAME)}'
    db.init_app(app=app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists(path.join(path.dirname(__file__), DB_NAME)):
            db.create_all()
            print("Database Created Successfully!")
