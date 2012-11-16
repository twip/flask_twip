#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import os
import glob

from .exception import TwipError


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
