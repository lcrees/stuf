# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .core import stuf

istuf = stuf 
    
from .special import defaultstuf, orderedstuf

idefaultstuf = defaultstuf
iorderedstuf = orderedstuf

from .restricted import fixedstuf, frozenstuf

ifixedstuf = fixedstuf
ifrozenstuf = frozenstuf