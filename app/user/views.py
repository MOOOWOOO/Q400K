# coding: utf-8
from flask import render_template

from app.util.decorators import login_required_
from . import user
from .models import User, UserDetail

__author__ = 'Jux.Liu'


@user.route('/<int:user_id>/', methods=['GET', 'POST'])
@login_required_
def user_main(user_id):
    u = User.query.get(user_id)
    ud = UserDetail.query.get(user_id)
    return render_template('user_pages/user_detail.html', user=u, user_detail=ud)
