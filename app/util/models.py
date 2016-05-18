# coding: utf-8
import uuid
import datetime

from app import db

__author__ = 'Jux.Liu'


class SerializeMixin(object):
    'Mixin for retrieving public fields of model in json-compatible format'
    __public__ = None
    __exclude__ = None

    def to_json(self, exclude=None, include=None, only=None, with_entities=None, join=None, parent=True, convert=True,
                **kwargs):
        """
        Returns model's PUBLIC data for jsonify
            exclude: 在转化时指定需要排除的字段列表
            include: 在转化时指定需要包含的字段列表
            only   : 在转化时指定仅仅包含的字段列表
            convert: 附加转换结果显示,当需要转换值的显示成指定的状态值使用, 状态值需要在kwargs指定.\
                     {'status': {'0': u'正常', '1': u'故障',...}}, 将会在返回的字段中附加一个同名的且前面加'_'的字段,\
                     当status的值为'0'时, 那返回值会附加的'_status'字段,且'_status'字段值为u'正常'.
            当存在外键的时候, 会获取外键中是否有'__showname__'方法,有的化将显示一个友好的值.
        """

        data = {}
        items = self._sa_instance_state.attrs.items()
        # items = self.__dict__.items()
        # column_name = self._sa_instance_state.attrs.keys()
        column_name = self.__table__.columns.keys()
        if parent:
            baseclass = self.__class__.__base__
            if hasattr(baseclass, '_sa_class_manager'):
                column_name = set(
                    column_name) | set(baseclass.__table__.columns.keys())
        # self.convert = convert
        # self.kwargs = kwargs
        to_dict = kwargs.pop('to_dict', False)

        if self.__public__ and self.__exclude__ is None:
            """ __public__ is True and __exclude__ is False """
            _public = self.__public__
            _exclude = []
        elif self.__public__ is None and self.__exclude__:
            """ __public__ is False and __exclude__ is True """
            _public = []
            _exclude = self.__exclude__
        elif self.__public__ and self.__exclude__:
            """ __public__ is True and __exclude__ is True """
            _exclude = self.__exclude__
            _public = set(self.__public__) - set(_exclude)
        else:
            """ __public__ is False and __exclude__ is False """
            _public = column_name
            _exclude = []

        if exclude:
            """ If you specify the parameters of exclude """
            _exclude = set(_exclude + exclude)

        if include:
            """ If you specify the parameters of include """
            _public = set(_public + include) - set(_exclude)

        if only:
            with_entities = only
        if with_entities:
            """ If you specify the parameters of only """
            _public = set(with_entities)
            _exclude = set([])

        for key, field in items:
            if _public and key not in _public:
                continue
            if key in _exclude:
                continue
            value = field.value
            if not to_dict:
                value = self._serialize(value)
            data[key] = value
            if convert and kwargs and kwargs.has_key(key):
                _key = '_%s' % key
                data[_key] = kwargs[key].get(value, value)
        if isinstance(join, dict):
            data.update(join)
        elif isinstance(join, list):
            for i in join:
                data.update(i)
        return data

    def to_dict(self, exclude=None, include=None, only=None, with_entities=None, join=None, parent=True, convert=True,
                **kwargs):
        return self.to_json(exclude, include, only, with_entities, join, parent, convert, to_dict=True, **kwargs)

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        ret = value

        if isinstance(value, datetime.datetime):
            ret = value.isoformat()
            # ret = value.strftime('%F %T')
        elif isinstance(value, datetime.date):
            ret = value.isoformat()
            # ret = value.strftime('%F')
        elif isinstance(value, uuid.UUID):
            ret = str(value)
        # elif hasattr(value, '__iter__'):
        #     # Don't set True
        #     if follow_fk:
        #         ret = []
        #         for v in value:
        #             ret.append(cls._serialize(v))
        # elif SerializeMixin in value.__class__.__bases__:
        #     try:
        #         ret = value._get_public()
        #     except:
        #         pass

        return ret


class CRUDMixin(SerializeMixin):
    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def save(self):
        """Saves the object to the database."""
        db.session.add(self)
        try:
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self, real_del=True):
        """Delete the object from the database."""
        if not real_del:
            self.visable = False
            db.session.add(self)
        else:
            db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
