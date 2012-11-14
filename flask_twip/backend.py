#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import os

class Backend(object):
    def save(self, key, string, force=False):
        raise NotImplementedError('You should use subclass of Backend')
    def load(self, key):
        raise NotImplementedError('You should use subclass of Backend')


class FileBackend(Backend):

    def __init__(self, folder=None):
        self.folder = folder

    def save(self, key, string, force=False):
        file = '%s/%s' % (self.folder, key)

        if not force and os.path.isfile(file):
            raise TypeError('File %s exists. Overwrite with force option')

        with open(file, 'w') as f:
            f.write(string)

    def load(self, key):
        file = '%s/%s' % (self.folder, key)
        with open(file, 'r') as f:
            return f.read()
