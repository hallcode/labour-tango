import os

from flask import Flask, g

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from . import config as default_config
from .models import import_all_models


# Global Libraries
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    """Initialise and set up the core application"""

    # Set up configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(default_config)

    config_path = os.path.join(app.instance_path, 'config.py')
    app.config.from_pyfile(config_path, silent=True)

    # Static files
    app.static_folder = app.config.get('STATIC_FOLDER')
    app.static_url_path = app.config.get('STATIC_URL_PATH')

    _init_db(app)
    _init_plugins(app)
    _register_services(app)
    _register_views(app)

    return app


def _init_db(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

    db.init_app(app)
    import_all_models()


def _init_plugins(app):
    """Initialise plugins"""
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "error"


def _register_services(app):
    from .services import login


def _register_views(app):
    from .views import home_bp, auth_bp, email_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_bp)