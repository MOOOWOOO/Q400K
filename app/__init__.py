# coding: utf-8

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

__author__ = 'Jux.Liu'

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)

    from .config import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)

    db.init_app(app=app)
    login_manager.init_app(app=app)

    return app
