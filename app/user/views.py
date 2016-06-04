# coding: utf-8
from math import ceil

from flask import render_template, request, jsonify

from app import db
from app.util.decorators import login_required_, root_required
from sqlalchemy import desc
from . import user
from .models import User, UserDetail

__author__ = 'Jux.Liu'


@user.route('/<int:user_id>/', methods=['GET', 'POST'])
@login_required_
def user_main(user_id):
    user_ = User.query.get(user_id)
    user_detail = UserDetail.query.get(user_id)
    return render_template('user/detail.html', user=user_, user_detail=user_detail)


@user.route('/list/')
@user.route('/list/<int:page>/')
@root_required
def list(page=1):
    user_db = User.query
    user_pages = int(ceil(user_db.count() / 50.0))
    user_list = user_db.filter_by(visable=True).order_by(desc(User.id)).offset(50 * (page - 1)).limit(50).all()
    return render_template('user/list.html', users=user_list, number=page, total=user_pages)


@user.route('/delete/', methods=['POST'])
@root_required
def delete():
    delete_list = User.query.filter(User.id.in_(request.get_json()['user_delete_list'])).all()
    user_list=list()
    for user_ in delete_list:
        if user_.role_id != 99:
            user_.role_id = 99
            user_list.append(user_)

    db.session.add_all(user_list)
    db.session.commit()
    return jsonify({'code': 1})

