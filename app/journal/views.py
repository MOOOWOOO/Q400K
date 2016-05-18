# coding: utf-8
from datetime import datetime
from math import ceil

from app import db
from app.main.decorator import login_required_
from app.main.views import verify_user
from flask import render_template, request, jsonify, url_for, redirect
from flask.ext.login import current_user
from sqlalchemy import desc
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
    del_journal.delete(False)
    return jsonify({'result': 'ok'})


@journal.route('/all-reset/<string:password>')
@login_required_
def reset(password):
    u = verify_user(username=current_user.username, password=password)
    if u:
        journal_list = Journal.query.filter_by(visable=False)
        for j in journal_list:
            j.visable = True
        db.session.add_all(journal_list)
        db.session.commit()
        return redirect(url_for('.list', page=1))
