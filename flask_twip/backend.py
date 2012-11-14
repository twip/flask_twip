#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import os
import glob

class Backend(object):
    def save(self, user, key, string):
        raise NotImplementedError('You should use subclass of Backend')
    def load(self, user, key):
        raise NotImplementedError('You should use subclass of Backend')


class FileBackend(Backend):

    def __init__(self, folder=None):
        self.folder = folder

    def save(self, user, key, string):
        for f in glob.glob('%s/%s.*' % (self.folder, user)):
            os.remove(f)

        with open('%s/%s.%s' % (self.folder, user, key), 'w') as f:
            f.write(string)

    def load(self, user, key):
        file = '%s/%s.%s' % (self.folder, user, key)
        with open(file, 'r') as f:
            return f.read()
