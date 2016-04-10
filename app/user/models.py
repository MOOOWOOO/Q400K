# coding: utf-8

from datetime import datetime

from app import db, login_manager
from app.util.models import CRUDMixin
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

__author__ = 'Jux.Liu'


class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)
    role_id = db.Column(db.Integer, nullable=False, default=2)

    def __repr__(self):
        return '<User #{0}: {1}, email: {2}, role #{3}>'.format(self.id, self.username, self.email, self.role_id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password=password)

    def verify_password(self, password):
        if self._password is None or password is None:
            return False
        return check_password_hash(self._password, password)

    def generate(self):
        self.save()
        ud = UserDetail(id=self.id)
        ud.save()
        return self

    @staticmethod
    @login_manager.user_loader
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def is_exists(column, value):
        return db.session.query(db.exists().where(column == value)).scalar()


DEFAULT_AVA_URL = '/static/images/default_avatar.jpg'


class UserDetail(db.Model, CRUDMixin):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    career = db.Column(db.Integer, nullable=True, unique=False)
    hometown = db.Column(db.Integer, nullable=True, unique=False)
    join_time = db.Column(db.Date, nullable=False, unique=False,
                          default=datetime.utcnow)
    avatar = db.Column(db.String, nullable=False, unique=False, default=DEFAULT_AVA_URL)

    def __repr__(self):
        return '<UserDetail #{0}: {1} Joined.>'.format(self.id, self.join_time)
