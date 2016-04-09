# coding: utf-8
import json

from app import db
from app.main.decorator import login_required_
from app.main.models import LoginForm, RegistForm, ChangePasswordForm
from app.user.models import User
from flask import render_template, request, redirect, url_for, send_from_directory
from flask.ext.login import current_user, logout_user, login_user
from . import main

__author__ = 'Jux.Liu'


@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        pass
    return render_template('index.html', user=None)


@main.route('/favicon.ico')
def favicon():
    """
站点图标设置
    :param: null
    :return:
    """
    return send_from_directory('static/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index', user=None))
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        u = User.query.filter_by(username=username).first()
        if u.verify_password(password=password):
            login_user(u)
            return redirect(request.args.get('next') or url_for('main.index', user=u))
        else:
            return json.dumps({'code': 2, 'msg': 'Username/Password Error'})
    return render_template("login.html", form=form)


@main.route('/regist/', methods=['GET', 'POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('regist.html', form=form)


@main.route('/logout/')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.login'))


@main.route('/change-password', methods=['GET', 'POST'])
@login_required_
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('main.logout'))
    return render_template('user_pages/change_password.html', form=form)
