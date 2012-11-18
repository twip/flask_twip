#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

class Environment(object):
    def __init__(self, request):
        self._request = request

    def isHTTPS(self):
        raise NotImplementedError('You should use subclass of Environment')

class CGIEnvironment(Environment):
    def isHTTPS(self):
        return ('HTTPS' in os.environ and os.environ.get('HTTPS') == 'on')

class HerokuEnvironment(Environment):
    def isHTTPS(self):
        return ('x-forwarded-proto' in request.headers and request.headers.get('x-forwarded-proto') == 'HTTPS')

class DevEnvironment(Environment):
    def isHTTPS(self):
        return ('wsgi.url_scheme' in os.environ and os.environ.get('wsgi.url_scheme') == 'https')
