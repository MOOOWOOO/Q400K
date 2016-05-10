# coding: utf-8
from flask import render_template, request, jsonify
from sqlalchemy import desc, asc
from math import ceil
from datetime import datetime

from app.main.decorator import login_required_
from . import journal
from .models import Journal

__author__ = 'Jux.Liu'


@journal.route('/list/')
@journal.route('/list/<int:page>/')
@login_required_
def list(page=1):
    journal_db = Journal.query
    journal_pages = int(ceil(journal_db.count() / 50.0))
    journal_list = journal_db.filter_by(visable=True).order_by(desc(Journal.id)).offset(50 * (page - 1)).limit(50).all()
    return render_template('journal/list.html', journals=journal_list, number=page, total=journal_pages)


@journal.route('/search/', methods=['POST'])
@login_required_
def search():
    param = request.get_json()
    # todo: do search and return


@journal.route('/new-record/', methods=['POST'])
@login_required_
def new_record():
    param = request.get_json()
    new_journal = Journal(level=param['level'],
                          title=param['title'],
                          detail=param['detail'],
                          datetime=datetime.now())
    new_journal.save()
    return jsonify({'result': 'ok', 'id': new_journal.id})


@journal.route('/delete/', methods=['POST'])
@login_required_
def delete_record():
    param = request.get_json()
    del_journal = Journal.query.filter_by(id=param['id']).first_or_404()
    del_journal.visable = False
    del_journal.save()
    return jsonify({'result': 'ok'})
