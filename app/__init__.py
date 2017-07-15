from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import config

bootstrap = Bootstrap()
mongo = PyMongo()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'warning'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
