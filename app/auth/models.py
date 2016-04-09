# coding: utf-8
from app import db

__author__ = 'Jux.Liu'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)

    def __repr__(self):
        return '<Role #{0}: {1}>'.format(self.id, self.name)

    def generate(self):
        self.save()
        return self

    @staticmethod
    def get_by_id(auth_id):
        return Role.query.get(auth_id)
