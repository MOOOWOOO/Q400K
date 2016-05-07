# coding: utf-8
from flask import Blueprint

__author__ = 'Jux.Liu'

journal = Blueprint('journal', __name__)

from . import views
