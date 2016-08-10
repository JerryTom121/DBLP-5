# -*- coding: utf-8 -*-
"""Auxiliary functions that support the crawler."""

from collections import namedtuple


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
