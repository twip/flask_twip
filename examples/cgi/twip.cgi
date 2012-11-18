#!/usr/bin/env python

# Use your virtualenv python as the shebang

try:
    from wsgiref.handlers import CGIHandler
    from flask import Flask, request
    from flask.ext.twip import Twip
    from flask.ext.twip.backend import FileBackend
    from flask.ext.twip.environment import CGIEnvironment
    import sys
    import os
    import logging
except Exception as e:
    print("Content-type: text/html")
    print('')
    print(repr(e))

if __name__ == '__main__':
    try:
        app = Flask(__name__, static_folder=None)
        app.config.from_object('settings')
        be = FileBackend(folder='/home/yegle/cgi-bin/tokens')
        e = CGIEnvironment()
        twip = Twip(app, backend=be, url='/', environment=e)

        CGIHandler().run(app)
    except Exception as e:
        print("Content-type: text/html")
        print("")
        print(repr(e))
