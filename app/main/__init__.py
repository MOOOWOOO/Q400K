# coding: utf-8
from flask import Blueprint

__author__ = 'Jux.Liu'

main = Blueprint('main', __name__)

from . import views
from . import decorator