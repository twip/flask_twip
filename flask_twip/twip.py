#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import requests
from flask import request as req
from flask import redirect, url_for, Blueprint

class Twip(object):

    def __init__(self, app=None, url='/twip'):
        self.url = url
        self.bp = Blueprint('twip', __name__, url_prefix=self.url)
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app

        self.bp.add_url_rule('/o/<path:path>', view_func=self.OMode)
        self.bp.add_url_rule('/t/<path:path>', view_func=self.TMode)
        self.bp.add_url_rule('/o/', view_func=self.redirect)
        self.bp.add_url_rule('/t/', view_func=self.redirect)
        self.bp.add_url_rule('/', view_func=self.index)

        self.app.register_blueprint(self.bp)

    def OMode(self, path):
        return path

    def TMode(self, path):
        return path

    def redirect(self):
        return redirect(url_for('twip.index'))

    def index(self):
        return 'index'
