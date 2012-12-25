#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

def allow_post(func):
    func.methods = ['POST', 'GET']
    return func
