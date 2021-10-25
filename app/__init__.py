from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_login import LoginManager
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login.init_app(app) 

    login.login_view = 'login'
    login.login_message = "you can't be here!"
    login.login_message_category = 'danger'

    with app.app_context():
        from app.blueprints.blog import bp as blog
        app.register_blueprint(blog)

        from app.blueprints.auth import bp as auth
        app.register_blueprint(auth)

        from app.blueprints.shop import bp as shop
        app.register_blueprint(shop)

        from . import routes, tokens

    return app
