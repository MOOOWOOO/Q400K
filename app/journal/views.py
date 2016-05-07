# coding: utf-8
from flask import render_template
from sqlalchemy import desc

from app.main.decorator import login_required_
from . import journal
from .models import Journal

__author__ = 'Jux.Liu'


@journal.route('/list/<int:page>/')
@login_required_
def list(page):
    journal_list = Journal.query.order_by(desc(Journal.id)).offset(50 * (page - 1)).limit(50 * page).all()
    return render_template('journal/list.html', journals=journal_list)
