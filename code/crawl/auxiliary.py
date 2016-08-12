# -*- coding: utf-8 -*-
"""Auxiliary functions that support the crawler."""

import random
from collections import namedtuple

from utils import parameters as params

Publisher = namedtuple('Publisher', ['name', 'href'])
Series = namedtuple('Series', ['text', 'href'])
Citation = namedtuple('Citation', ['reference', 'label'])


def first_or_none(seq):
    """."""
    try:
        return next(iter(seq))
    except StopIteration:
        pass


def get_fullname(o):
    """get the full name of the class."""
    return '%s.%s' % (o.__module__, o.__class__.__name__)


def random_sleep():
    """decide a random time to sleep."""
    return random.uniform(1, params.DOWNLOAD_DELAY)
