# coding: utf-8
from datetime import datetime

from app import db
from app.util.models import CRUDMixin

__author__ = 'Jux.Liu'


class Journal(db.Model, CRUDMixin):
    __tablename__ = 'journal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.now())
    level = db.Column(db.Integer, nullable=False, unique=False, default=0)
    title = db.Column(db.String, nullable=False, unique=False)
    detail = db.Column(db.Text, nullable=False, unique=False)
    visable = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Journal #{0}: Level-{1} DateTime: {2}>'.format(self.id, self.level, self.datetime)

    @staticmethod
    def get_by_id(journal_id):
        return Journal.query.get(journal_id)

    @staticmethod
    def generate_fake(count=1000):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py
        seed()
        for i in range(count):
            j = Journal(datetime=forgery_py.date.date(),
                        level=randint(0, 5),
                        title=forgery_py.lorem_ipsum.sentence(),
                        detail=forgery_py.lorem_ipsum.paragraph())
            db.session.add(j)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
