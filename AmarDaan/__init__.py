from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "amardaan.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mamunapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app=app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('AmarDaan/' + DB_NAME):
            db.create_all()
            print("Database Created Successfully!")

# Ensure that the following code block is only executed if this script is run directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
