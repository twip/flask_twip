#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import requests
from flask import request as req
from flask import redirect

class Twip(object):

    def __init__(self, app=None, url='twip'):
        self.url = url
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app

        self.app.add_url_rule('/%s/o/<path:path>' % (self.url,), view_func=self.OMode)
        self.app.add_url_rule('/%s/t/<path:path>' % (self.url,), view_func=self.TMode)
        self.app.add_url_rule('/%s/o/' % (self.url,), view_func=self.redirect)
        self.app.add_url_rule('/%s/t/' % (self.url,), view_func=self.redirect)
        self.app.add_url_rule('/%s/' % (self.url,), view_func=self.index)

    def OMode(self, path):
        return path

    def TMode(self, path):
        return path

    def redirect(self):
        return redirect(url_for('index'))

    def index(self):
        return 'index'
