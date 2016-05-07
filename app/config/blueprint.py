# coding: utf-8
from app.journal import journal as journal_bp
from app.main import main as main_bp
from app.user import user as user_bp

__author__ = 'Jux.Liu'


def regist(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(journal_bp, url_prefix='/journal')
