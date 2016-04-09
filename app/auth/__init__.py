# coding: utf-8
from flask import Blueprint

__author__ = 'Jux.Liu'

auth = Blueprint('auth', __name__)

from . import views
from . import models
