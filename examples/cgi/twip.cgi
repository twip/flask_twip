#!/usr/bin/env python

try:
    from wsgiref.handlers import CGIHandler
    from flask import Flask
    from flask_twip import Twip
    from flask_twip.backend import FileBackend
    from flask import request
    from flask_twip.environment import CGIEnvironment
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
