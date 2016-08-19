# -*- coding: utf-8 -*-
"""parse the crawled publication."""

import json
from os.path import join
from utils.logger import Logger
from utils import auxiliary as auxi
from utils import opfiles as op


class BasicParsing(object):
    """a class used to do the basic parsing."""

    def __init__(self, path_root):
        """init."""
        self.log = Logger.get_logger(auxi.get_fullname(self))
        self.path_root = path_root

    def init_path(self, file_to_parse):
        """init some basic paths."""
        self.log.info("init path...")
        self.path_raw = join(self.path_root, "db",
                             "backup_file", file_to_parse)
        self.path_parsed = join(self.path_root, "db",
                                "parsed_file", file_to_parse)
        self.path_listof_download = join(
            self.path_root, "publications_to_download")
        return self

    def parse_file(self):
        """read and init file."""
        self.log.info("read big json file...")
        raw_data = op.read_txt(self.path_raw)
        self.log.info("process each single json...")
        files = []
        for ind, line in enumerate(raw_data):
            single_json = json.loads(line)
            single_json.pop('_id')
            files.append(single_json)
            if ind % 5000 == 0:
                self.log.debug("parsed {i}/{t} json file.".format(
                    i=ind, t=len(raw_data)))
        return files

    def load_list_todownload(self):
        """load the file that is used to download."""
        self.log.info("load the list_to_download")
        list_todownload = op.read_txt(self.path_listof_download)
        return set(map(str.lower, list_todownload))
