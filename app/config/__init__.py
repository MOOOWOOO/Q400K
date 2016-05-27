# coding: utf-8
from datetime import timedelta
from getpass import getuser

from os import environ
from os.path import abspath, dirname
from . import blueprint
from .errors import configure_errorhandlers

__author__ = 'Jux.Liu'


class Config():
    SECRET_KEY = environ.get('SECRET_KEY') or '42'
    FLASKY_ADMIN = environ.get('FLASKY_ADMIN')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = True
    WTF_CSRF_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']
    UPLOAD_PATH = r'/home/pi/Documents/demo/' if getuser() == 'pi' else r'/home/jux/Documents/Q400K/'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)

    @staticmethod
    def init_app(app):
        configure_errorhandlers(app)
        blueprint.regist(app)


basedir = abspath(dirname(__file__))


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:////home/jux/Documents/Q400K/data.sqlite'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL') or 'sqlite:////home/jux/Documents/Q400K/data-dev.sqlite'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URL') or 'sqlite:////home/jux/Documents/Q400K/data-test.sqlite'


config = {
    'default'   : DevelopmentConfig,
    'testing'   : TestingConfig,
    'production': ProductionConfig,
    'develop'   : DevelopmentConfig
}
