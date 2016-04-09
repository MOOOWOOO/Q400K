# coding: utf-8
from app.main import main as main_bp
from app.user import user as user_bp

__author__ = 'Jux.Liu'


def regist(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
