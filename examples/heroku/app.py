#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

from flask import Flask
from flask.ext.twip import Twip
from flask.ext.twip.backend import FileBackend
from flask.ext.twip.environment import HerokuEnvironment
import os

app = Flask(__name__)
app.config.from_object('settings')
be = FileBackend(folder='/tmp/twip')
twip = Twip(app, backend=be, environment=HerokuEnvironment)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port
    )
