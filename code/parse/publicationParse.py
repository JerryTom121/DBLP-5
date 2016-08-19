# -*- coding: utf-8 -*-
"""parse the crawled publication."""
from utils.logger import Logger
from utils import auxiliary as auxi
from parse.basicParsing import BasicParsing


class ParsePublications(BasicParsing):
    """a class used to parse the publication."""

    def __init__(self, path_root):
        """init."""
        super(ParsePublications, self).__init__([])
        self.log = Logger.get_logger(auxi.get_fullname(self))
        self.path_root = path_root
        self.init_path("publications.json")
        self.want_we_want = ["acronym", "venue_name", "year",
                             "key", "title", "authors"]

    def extract(self, files, list_todownload):
        """extract useful information.

        remove useless information,
        and only consider the publications that in the list_todownload.
        """
        valid_publications = []
        invalid_acronym = set()
        for ind, file in enumerate(files):
            acronym = file['acronym']
            if acronym.lower() in list_todownload:
                valid_publications.append([file[w] for w in self.want_we_want])
            else:
                invalid_acronym.add(acronym)
        self.log.info("the original size is: {t}; the valid size is {v}"
                      .format(t=len(files), v=len(valid_publications)))
        self.log.debug("the size of invalid acronym is: {s}, its content: {c}"
                       .format(s=len(invalid_acronym), c=invalid_acronym))
        return valid_publications

    def get_authors(self, files):
        """get a complete author list."""
        authors = []
        self.log.info("get a complete author list.")
        for file in files:
            authors += file[5]
        unique_authors = set(authors)
        self.log.info("the number of unique authors {a}".format(
            a=len(unique_authors)))
        return authors, unique_authors

    def parse(self):
        """parse the publication to something that we want."""
        files = self.parse_file()
        list_todownload = self.load_list_todownload()
        simplified_files = self.extract(files, list_todownload)
        authors, unique_authors = self.get_authors(simplified_files)
        return unique_authors
