# coding: utf-8

from flask import render_template, send_from_directory

from app.user.models import User
from flask.ext.login import current_user
from . import main

__author__ = 'Jux.Liu'



@main.route('/')
@main.route('/index/')
def index():
    if current_user.is_authenticated:
        pass
    return render_template('index.html')


@main.route('/favicon.ico')
def favicon():
    """
站点图标设置
    :param: null
    :return:
    """
    return send_from_directory('static/images', 'favicon.ico', mimetype='image/x-icon')


