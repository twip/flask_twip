#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

from flask import Flask
from flask.ext.twip import Twip

if __name__ == '__main__':
    app = Flask(__name__)
    twip = Twip(app)
    app.run(
        debug=True,
    )
