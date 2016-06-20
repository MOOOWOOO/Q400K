# coding: utf-8
from datetime import datetime
from math import ceil

from flask import render_template, request, jsonify, url_for, redirect

from app import db
from app.auth.views import verify_user
from app.util.decorators import login_required_, root_required
from app.util.file_manager import upload
from flask.ext.login import current_user
from os.path import getsize
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


@journal.route("/get/<int:id>/")
@login_required_
def get_by_id(id):
    journal_db = Journal.query
    journal_record = journal_db.filter_by(id=id, visable=True).first()
    journal_record = {
        'id'      : str(journal_record.id),
        'level'   : str(journal_record.level),
        'detail'  : str(journal_record.detail),
        'title'   : str(journal_record.title),
        'datetime': str(journal_record.datetime)
    }
    return jsonify({"journal": journal_record})


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
    if new_journal.save():
        new_journal = {
            'id'      : str(new_journal.id),
            'level'   : str(new_journal.level),
            'detail'  : str(new_journal.detail),
            'title'   : str(new_journal.title),
            'datetime': str(new_journal.datetime)
        }
        return jsonify({'result': 'ok', 'journal': new_journal})
    else:
        return jsonify({})


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


@journal.route('/import/', methods=['GET', 'POST'])
@root_required
def import_file():
    if request.method == 'GET':
        return render_template('journal/import.html')

    else:
        file_path = upload(request.files['upload'])
        file_size = getsize(file_path)
        if file_size == 0:
            return jsonify({'result': 'empty file'})

        else:
            if do_import(file_path=file_path, file_size=file_size):
                return jsonify({'result': 'ok'})
            else:
                return jsonify({'result': 'import error'})


def do_import(file_path, file_size):
    try:
        with open(file_path, 'r') as f:
            large_file = float(file_size / 1000000) > 100
            record_list = list()

            for line in f:
                param = line.split(' | ')
                new_record = Journal(level=param[0],
                                     title=param[1],
                                     detail=param[2],
                                     datetime=param[3])
                record_list.append(new_record)

                if large_file:
                    if len(record_list) > 10000:
                        db.session.add_all(record_list)
                        db.commit()
                        record_list = list()

                else:
                    pass

        if len(record_list) > 0:
            db.session.add_all(record_list)
            db.commit()

        return True

    except Exception as e:
        return False
