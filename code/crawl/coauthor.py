# -*- coding: utf-8 -*-
"""get an authors' coauthor information in DBLP."""

import requests
from lxml import etree

from lazyAPIData import LazyAPIData
from utils import parameters as params


class CoAuthor(LazyAPIData):

    """
    Represents the coauthor information of a DBLP author.
    All data but the author's key is lazily loaded.
    Fields that aren't provided by the underlying XML are None.

    Attributes:
    author - the author's information, e.g., urlpt, author
    coauthor information - the coauthor information for a given author,
    it will return {coauthor name: {urlpt, count}}.
    """

    def __init__(self, urlpt):
        """initialization."""
        self.urlpt = urlpt
        self.xml = None
        super(CoAuthor, self).__init__(['author', 'coauthors'])

    def load_data(self):
        """load data of author."""
        resp = requests.get(params.DBLP_COAUTHORS_URL.format(urlpt=self.urlpt))

        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        data = {
            'author': root.attrib,
            'coauthors': {author.text: author.attrib for author in
                          root.xpath('/coauthors/author[@urlpt]')}
        }
        self.data = data
