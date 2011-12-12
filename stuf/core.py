# -*- coding: utf-8 -*-
'''core stuf'''

from __future__ import absolute_import

from .base import writestuf


class stuf(writestuf, dict):

    '''dictionary with dot attributes'''