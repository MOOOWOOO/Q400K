# coding: utf-8
from app.main.decorator import login_required_
from flask import render_template
from . import user
from .models import User

__author__ = 'Jux.Liu'


@user.route('/<int:user_id>/', methods=['GET', 'POST'])
@login_required_
def user_main(user_id):
    u = User.query.get(user_id)
    return render_template('user_pages/user_detail.html', user=u)
