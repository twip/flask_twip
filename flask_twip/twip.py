#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

import requests
from flask import request as req
from flask import redirect, url_for, Blueprint,\
    session, request, render_template, abort, \
    make_response
from flask.ext.oauth import OAuth, OAuthException

import random
import string
import json
import os
import re

from .backend import TokenLoadingError, TokenSavingError
from urllib import urlencode


class Twip(object):

    version_re = re.compile(r'^[0-9]+(?:\.[0-9]+)?$')
    default_version = 1.1

    def __init__(
        self,
        app=None,
        url='/twip',
        backend=None,
        environment=None
    ):
        self.url = os.path.normpath(url)
        self.bp = Blueprint(
            'twip',
            __name__,
            url_prefix=None if self.url == '/' else self.url,
            template_folder='templates',
            static_folder='static',
        )

        if app is not None:
            self.app = app
            self.init_app(self.app)
            self.app.wsgi_app = environment(self.app.wsgi_app)
        else:
            self.app = None

        self.backend = backend
        self.token = None

    @property
    def o_base(self):
        try:
            return self._o_base
        except AttributeError:
            self._o_base = '%s%s' % (
                request.environ['twip_base_url'],
                os.path.dirname(
                    # FIXME: I'm not sure the best way to extract this info
                    self.app.url_map._rules_by_endpoint['twip.OMode'][0].rule
                )
            )
            return self._o_base

    @property
    def t_base(self):
        try:
            return self._t_base
        except AttributeError:
            self._t_base = '%s%s' % (
                request.environ['twip_base_url'],
                os.path.dirname(
                    # FIXME:
                    self.app.url_map._rules_by_endpoint['twip.TMode'][0].rule
                )
            )
            return self._t_base

    def getMapper(self):
        m = (
            ('/o/<path:path>', self.OMode),
            ('/t/<path:path>', self.TMode),
            ('/o/', self.redirect),
            ('/t/', self.redirect),
            ('/', self.index),
            ('/oauth/start/', self.oauth_start),
            ('/oauth/callback/', self.oauth_callback),
            ('/show_api/', self.show_api),
        )
        return m

    def init_app(self, app):
        self.app = app

        for (url, func) in self.getMapper():
            self.bp.add_url_rule(url, view_func=func)

        self.app.register_blueprint(self.bp)

    def oauth_app(self, base_url='https://api.twitter.com/1.1/'):
        oauth = OAuth()
        twitter = oauth.remote_app(
            'twitter',
            base_url='',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key=self.app.config.get('TWITTER_CONSUMER_KEY'),
            consumer_secret=self.app.config.get('TWITTER_CONSUMER_SECRET'),
        )
        twitter.tokengetter(self.tokengetter)
        return twitter

    def tokengetter(self):
        if self.token:
            return (
                self.token['oauth_token'],
                self.token['oauth_token_secret']
            )
        else:
            return None

    def OMode(self, path):
        username, key = path.split('/')[:2]
        try:
            token = self.backend.load(username, key)
            self.token = json.loads(token)
        except TokenLoadingError as e:
            abort(401)

        remote_url = '/'.join(path.split('/')[2:])

        if remote_url == 'oauth/access_token':
            return urlencode(self.token)
        else:
            remote_url = self.url_fixer(remote_url)
            values = self.args_fixer(request.values)

            twitter = self.oauth_app()

            if request.method == 'POST':
                r = twitter.post(remote_url, data=values)
            elif request.method == 'GET':
                r = twitter.get(remote_url, data=values)

            return make_response((r.raw_data, r.status, r.headers))

    OMode.methods = ['GET', 'POST']

    def TMode(self, path):
        remote_url = self.url_fixer(path)
        values = self.args_fixer(request.values)
        headers = {k:v for k,v in request.headers if k in self.getTModeForwaredHeaders()}

        if request.method == 'POST':
            r = requests.post(remote_url, data=values)
        elif request.method == 'GET':
            r = requests.get(remote_url, params=values)

        return r.text

    TMode.methods = ['GET', 'POST']

    def getTModeForwaredHeaders(self):
        return [
            'Host',
            'User-Agent',
            'Authorization',
            'Content-Type',
            'X-Forwarded-For',
            'Expect',
        ]

    def url_fixer(self, url):
        # determine if there's any version info
        first_part = url.split('/')[0]
        if first_part.startswith('search.'):
            url = 'http://search.twitter.com/%s' % (url,)
        elif not self.version_re.match(first_part) \
                and first_part not in ('i', 'oauth'):
            # no version info
            # not unversioned API request
            # we need prepend the url with default version
            url = 'https://api.twitter.com/%s/%s' % (self.default_version, url)
        else:
            url = 'https://api.twitter.com/%s' % (url,)

        for key, replacement in self.url_replacements():
            url.replace(key, replacement)

        return url

    def url_replacements(self):
        return (
            ('i/search.json', 'search.json'),
        )

    def args_fixer(self, args):
        ret = dict()
        for key in args:
            if key in ('pc', 'earned'):
                ret[key] = False
            else:
                ret[key] = args[key]

        return ret

    def redirect(self):
        return redirect(url_for('twip.index'))

    def index(self):
        return render_template('base.jinja')

    def oauth_start(self):
        twitter = self.oauth_app()
        return twitter.authorize(callback=url_for('twip.oauth_callback'))

    def oauth_callback(self):
        twitter = self.oauth_app()
        try:
            if 'oauth_verifier' in request.args:
                data = twitter.handle_oauth1_response()
            elif 'code' in request.args:
                data = twitter.handle_oauth2_response()
            else:
                data = twitter.handle_unknown_response()
        except OAuthException as e:
            return redirect(url_for('twip.index'))
        twitter.free_request_token()

        key = ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for x in range(5)
        )

        self.backend.save(data['screen_name'], key, json.dumps(data))

        url = '%s/%s/%s/' % (
            self.o_base,
            data['screen_name'],
            key
        )

        return redirect(url_for('twip.show_api') + '?api=%s' % (url,))

    def show_api(self):
        api = request.args.get('api', self.t_base + '/')
        return render_template('show_api.jinja', api=api)
