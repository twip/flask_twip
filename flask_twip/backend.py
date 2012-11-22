#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import os
import glob

from .exception import TwipError

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, String


class TokenLoadingError(TwipError):
    pass


class TokenSavingError(TwipError):
    pass


class Backend(object):
    def save(self, user, key, string):
        raise NotImplementedError('You should use subclass of Backend')

    def load(self, user, key):
        raise NotImplementedError('You should use subclass of Backend')


class FileBackend(Backend):

    def __init__(self, folder=None):
        self.folder = folder
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

    def save(self, user, key, string):
        try:
            for f in glob.glob('%s/%s.*' % (self.folder, user)):
                os.remove(f)

            with open('%s/%s.%s' % (self.folder, user, key), 'w') as f:
                f.write(string)
        except Exception as e:
            raise TokenSavingError(str(e))

    def load(self, user, key):
        try:
            file = '%s/%s.%s' % (self.folder, user, key)
            with open(file, 'r') as f:
                return f.read()
        except Exception as e:
            raise TokenLoadingError(str(e))


class SQLBackend(Backend):
    def __init__(self, db=None, table=None):
        engine = create_engine(db, convert_unicode=True)
        self.session = scoped_session(
            sessionmaker(bind=engine)
        )
        Base = declarative_base()
        Base.query = self.session.query_property()
        self.base = Base
        self.engine = engine

        class Token(Base):
            __tablename__ = table

            id = Column(Integer, primary_key=True)
            user = Column(String, unique=True)
            key = Column(String)
            string = Column(String)

            def __init__(self, user, key, string):
                self.user = user
                self.key = key
                self.string = string

        self.model = Token

    def save(self, user, key, string):
        try:
            token = self.model(user, key, string)
            self.session.add(token)
            self.session.query(self.model).filter(
                self.model.user == user,
                self.model.key != key
            ).delete()
            self.session.commit()
        except Exception as e:
            raise TokenSavingError(str(e))

    def load(self, user, key):
        try:
            token = self.session.query(self.model).filter_by(user=user, key=key).first()
            return token.string
        except Exception as e:
            raise TokenLoadingError(str(e))

    def init_db(self):
        self.base.metadata.create_all(self.engine)
