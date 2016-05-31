# coding: utf-8
from flask import current_app
from os.path import join
from werkzeug.utils import secure_filename

__author__ = 'Jux.Liu'

ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload(request_file):
    f = request_file
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        file_path=join(current_app.config['UPLOAD_PATH'], filename)
        f.save(file_path)
        return file_path
    else:
        return 0
