# coding: utf-8
from app import db
from app.user.models import User
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

__author__ = 'Jux.Liu'


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


class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Hometown(db.Model):
    __tablename__ = 'hometown'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
