# -*- coding: utf-8 -*-
"""A file to define the logger."""

import logging
import logging.config


class Logger:
    """docstring"""

    @staticmethod
    def get_logger(name=None,
                   level=logging.DEBUG):
        """define the name of logger."""
        logging.config.fileConfig('settings/logging.conf')
        return logging.getLogger(name)
