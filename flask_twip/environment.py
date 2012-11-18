#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

from flask import request

class Environment(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['twip_base_url'] = '%s://%s' % (environ['twip_scheme'], environ['HTTP_HOST'])
        return self.app(environ, start_response)

class CGIEnvironment(Environment):

    def __call__(self, environ, start_response):
        environ['twip_scheme'] = 'https' if ('HTTPS' in environ and environ.get('HTTPS') == 'on') else 'http'
        pathInfo = environ.get('PATH_INFO')
        scriptURL = environ.get('SCRIPT_URL')
        if scriptURL.endswith(pathInfo):
            environ['twip_base_url'] = '%s://%s%s' % (environ['twip_scheme'], environ['HTTP_HOST'], scriptURL[:-len(pathInfo)])
        else:
            environ['twip_base_url'] = '%s://%s' % (environ['twip_scheme'], self['HTTP_HOST'])

        return self.app(environ, start_response)

class WSGIEnvironment(Environment):

    def __call__(self, environ, start_response):
        environ['twip_scheme'] = 'https' if ('wsgi.url_scheme' in environ and environ.get('wsgi.url_scheme') == 'https') else 'http'
        return super(WSGIEnvironment, self).__call__(environ, start_response)

class HerokuEnvironment(WSGIEnvironment):
    def __call__(self, environ, start_response):
        environ['wsgi.url_scheme'] = environ['HTTP_X_FORWARDED_PROTO']
        return super(HerokuEnvironment, self).__call__(environ, start_response)
