# coding: utf-8
from app import db

__author__ = 'Jux.Liu'


class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class Hometown(db.Model):
    __tablename__ = 'hometown'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
