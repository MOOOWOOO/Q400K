# coding: utf-8
from app import db
from app.user.models import User
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

__author__ = 'Jux.Liu'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)

    def __repr__(self):
        return '<Role #{0}: {1}>'.format(self.id, self.name)

    def generate(self):
        self.save()
        return self

    @staticmethod
    def get_by_id(auth_id):
        return Role.query.get(auth_id)


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember')
    submit = SubmitField('Login')


class RegistForm(Form):
    email = StringField('email', validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField('username', validators=[DataRequired(), Length(4, 20)])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('confirm password',
                              validators=[DataRequired(), EqualTo('password', message='Password not match.')])
    submit = SubmitField('Regist')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


class ChangePasswordForm(Form):
    oldpassword = PasswordField('old password', validators=[DataRequired()])
    newpassword = PasswordField('new password', validators=[DataRequired()])
    newpassword2 = PasswordField('confirm new password',
                                 validators=[DataRequired(), EqualTo('newpassword', message='Password not match.')])
    submit = SubmitField('Submit')
