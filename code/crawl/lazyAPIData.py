# -*- coding: utf-8 -*-
"""A auxiliary class.

A class should be imported in, e.g., author.py.
"""


class LazyAPIData(object):

    """A class."""

    def __init__(self, lazy_attrs):
        """."""
        self.lazy_attrs = set(lazy_attrs)
        self.data = None

    def __getattr__(self, key):
        """private function:getattr."""
        if key in self.lazy_attrs:
            if self.data is None:
                self.load_data()
            return self.data[key]
        raise AttributeError(key)

    def load_data(self):
        """left it for empty."""
        pass
