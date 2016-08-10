# -*- coding: utf-8 -*-
"""get authors' information in DBLP."""

import requests
from lxml import etree

from lazyAPIData import LazyAPIData
from publication import Publication
from utils import parameters as params


class Author(LazyAPIData):

    """
    Represents a DBLP author. All data but the author's key is lazily loaded.
    Fields that aren't provided by the underlying XML are None.

    Attributes:
    name - the author's primary name record
    publications - a list of lazy-loaded Publications results by this author
    homepages - a list of author homepage URLs
    homonyms - a list of author aliases
    """

    def __init__(self, urlpt):
        """initialization."""
        self.urlpt = urlpt
        self.xml = None
        super(Author, self).__init__(['name', 'publications', 'homepages',
                                      'homonyms'])

    def load_data(self):
        """load data of author."""
        resp = requests.get(params.DBLP_PERSON_URL.format(urlpt=self.urlpt))

        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        # print(etree.tostring(root, pretty_print=True))
        data = {
            'name': root.attrib['name'],
            'publications': [
                Publication(k) for k in
                root.xpath('/dblpperson/dblpkey[not(@type)]/text()')],
            'homepages': root.xpath(
                '/dblpperson/dblpkey[@type="person record"]/text()'),
            'homonyms': root.xpath('/dblpperson/homonym/text()')
        }

        self.data = data
