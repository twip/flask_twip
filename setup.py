#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals,\
    absolute_import, division, print_function

"""
Flask-Twip
----------

Flask-Twip is an extension of Flask microframework that can embed
Twitter API proxy feature into your website.

"""

from setuptools import setup, find_packages

setup(
    name='Flask-Twip',
    version='0.0.5',
    url='https://github.com/yegle/flask_twip/',
    license='MPL',
    author='yegle',
    author_email='flask_twip.python@yegle.net',
    description='twitter API proxy extension for Flask microframework',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask >= 0.9',
        'requests >= 0.14.2',
        'Flask-OAuth >= 0.12',
        'SQLAlchemy >= 0.7.9',
        'requests >= 0.14.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
