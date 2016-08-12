# -*- coding: utf-8 -*-
"""get publication' information in DBLP."""
import requests
from lxml import etree
from lazyAPIData import LazyAPIData
from utils import parameters as params
import auxiliary as auxi


class Publication(LazyAPIData):
    """
    Represents a DBLP publication- eg, article, inproceedings, etc.
    All data but the key is lazily loaded.
    Fields that aren't provided by the underlying XML are None.

    Attributes:
    type - the publication type, eg "article", "inproceedings", "proceedings",
    "incollection", "book", "phdthesis", "mastersthessis"
    sub_type - further type information, if provided- eg, "encyclopedia entry",
    "informal publication", "survey"
    title - the title of the work
    authors - a list of author names
    journal - the journal the work was published in, if applicable
    volume - the volume, if applicable
    number - the number, if applicable
    chapter - the chapter, if this work is part of a book or otherwise
    applicable
    pages - the page numbers of the work, if applicable
    isbn - the ISBN for works that have them
    ee - an ee URL
    crossref - a crossrel relative URL
    publisher - the publisher, returned as a (name, href) named tuple
    citations - a list of (text, label) named tuples representing cited works
    series - a (text, href) named tuple describing the containing series, if
    applicable
    """

    def __init__(self, key):
        """init."""
        self.key = key
        self.xml = None
        super(Publication, self).__init__(
              ['type', 'sub_type', 'mdate', 'authors', 'editors', 'title',
               'year', 'month', 'journal', 'volume', 'number', 'chapter',
               'pages', 'ee', 'isbn', 'url', 'booktitle', 'crossref',
               'publisher', 'school', 'citations', 'series'])

    def load_data(self):
        """fill in the function of load data."""
        resp = requests.get(params.DBLP_RECORDS_URL.format(key=self.key))
        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        publication = auxi.first_or_none(root.xpath('/dblp/*[1]'))
        if publication is not None:
            data = {
                'type': publication.tag,
                'sub_type': publication.attrib.get('publtype', None),
                'mdate': publication.attrib.get('mdate', None),
                'authors': publication.xpath('author/text()'),
                'editors': publication.xpath('editor/text()'),
                'title': auxi.first_or_none(publication.xpath('title/text()')),
                'year': auxi.first_or_none(publication.xpath('year/text()')),
                'month': auxi.first_or_none(publication.xpath('month/text()')),
                'journal': auxi.first_or_none(
                    publication.xpath('journal/text()')),
                'volume': auxi.first_or_none(
                    publication.xpath('volume/text()')),
                'number': auxi.first_or_none(
                    publication.xpath('number/text()')),
                'chapter': auxi.first_or_none(
                    publication.xpath('chapter/text()')),
                'pages': auxi.first_or_none(publication.xpath('pages/text()')),
                'ee': auxi.first_or_none(publication.xpath('ee/text()')),
                'isbn': auxi.first_or_none(publication.xpath('isbn/text()')),
                'url': auxi.first_or_none(publication.xpath('url/text()')),
                'booktitle': auxi.first_or_none(
                    publication.xpath('booktitle/text()')),
                'crossref': auxi.first_or_none(
                    publication.xpath('crossref/text()')),
                'publisher': auxi.first_or_none(
                    publication.xpath('publisher/text()')),
                'school': auxi.first_or_none(
                    publication.xpath('school/text()')),
                'citations': [
                    auxi.Citation(c.text, c.attrib.get('label', None))
                    for c in publication.xpath('cite') if c.text != '...'],
                'series': auxi.first_or_none(
                    auxi.Series(s.text, s.attrib.get('href', None))
                    for s in publication.xpath('series'))
            }
            self.data = data
