#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

from flask import request

class Environment(object):
    def isHTTPS(self):
        raise NotImplementedError('You should use subclass of Environment')

    def getHostname(self):
        raise NotImplementedError('You should use subclass of Environment')

    def getBaseURL(self):
        raise NotImplementedError('You should use subclass of Environment')

    def __getitem__(self, name):
        if name == 'scheme':
            return 'https' if self.isHTTPS() else 'http'
        elif name == 'hostname':
            return self.getHostname()
        elif name == 'base_url':
            return self.getBaseURL()

class CGIEnvironment(Environment):
    def isHTTPS(self):
        return ('HTTPS' in request.environ and request.environ.get('HTTPS') == 'on')

    def getHostname(self):
        return request.environ.get('HTTP_HOST')

    def getBaseURL(self):
        pathInfo = request.environ.get('PATH_INFO')
        scriptURL = request.environ.get('SCRIPT_URL')
        if scriptURL.endswith(pathInfo):
            return '%s://%s%s' % (self['scheme'], self['hostname'], scriptURL[:-len(pathInfo)])
        else:
            return None

class HerokuEnvironment(Environment):
    def isHTTPS(self):
        return ('x-forwarded-proto' in request.headers and request.headers.get('x-forwarded-proto') == 'HTTPS')

    def getHostname(self):
        return request.environ.get('HTTP_HOST')

class DevEnvironment(Environment):
    def isHTTPS(self):
        return ('wsgi.url_scheme' in request.environ and request.environ.get('wsgi.url_scheme') == 'https')

    def getHostname(self):
        return request.environ.get('HTTP_HOST')

    def getBaseURL(self):
        return '%s://%s' % (self['scheme'], self['hostname'])
