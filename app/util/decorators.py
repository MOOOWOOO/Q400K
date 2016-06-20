# coding: utf-8
from functools import wraps

from flask import current_app, redirect, url_for, request, jsonify

from flask.ext.login import current_user

__author__ = 'Jux.Liu'


def login_required_(func):
    """
    重写的login_required函数，用于验证当前访问用户是否登录
    :param func:
    :return:
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        return func(*args, **kwargs)

    return decorated_view


def root_required(func):
    """
    检查是否是超级管理员
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role_id == 0:
            return func(*args, **kwargs)
        else:
            return jsonify({'code': 3, 'msg': 'Permission denied, root required.'})

    return decorated_view
