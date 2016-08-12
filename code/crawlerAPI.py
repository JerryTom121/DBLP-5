# -*- coding: utf-8 -*-
"""A API entry for different functions of the crawler."""

import requests
from lxml import etree
from optparse import OptionParser

from crawl import Author
from crawl import CoAuthor
from crawl import Venues
from crawl import Publication
from utils import Logger
from utils import parameters as params


class CrawlerAPI(object):

    """a api for dblp crawler."""

    def __init__(self):
        """init."""
        self.log = Logger.get_logger("crawler_api")

    def crawl_author_assist(self, resp):
        """an assistant function to help the function 'crawl_author'."""
        parsed = []
        root = etree.fromstring(resp.content)
        # print(etree.tostring(root, pretty_print=True))
        for urlpt in root.xpath('/authors/author/@urlpt'):
            parsed.append(Author(urlpt))
        return parsed

    def crawl_author(self, o):
        """get an author's information in DBLP."""
        resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                            params={'xauthor': o.author})
        return self.crawl_author_assist(resp)

    def crawl_coauthor_assist(self, resp):
        """an assistant function to help the function 'crawl_coauthor'."""
        parsed = []
        root = etree.fromstring(resp.content)
        for urlpt in root.xpath('/authors/author/@urlpt'):
            parsed.append(CoAuthor(urlpt))
        return parsed

    def crawl_coauthor(self, o):
        """get an author's coauthor information in DBLP."""
        resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                            params={'xauthor': o.author})
        return self.crawl_coauthor_assist(resp)

    def crawl_venues_assist(self, resp, venue):
        """an assistant function to help the function 'crawl_venues'."""
        parsed = []
        root = etree.fromstring(resp.content)
        # print(etree.tostring(root, pretty_print=True))
        venues = [{x.tag: x.text for x in hit.xpath('info/*')}
                  for hit in root.xpath('//result/hits/hit')]
        venues = [v for v in venues
                  if v.get("acronym", "").lower() == venue.lower()]
        self.log.debug("retrieved venues: {v}".format(v=venues))
        for venue in venues:
            self.log.info("processing {v}".format(v=venue['venue']))
            parsed.append(Venues(venue))
        return parsed

    def crawl_venues(self, o):
        """get the information of a venue (conference/journal) in DBLP."""
        resp = requests.get(params.DBLP_VENUES_SEARCH_URL,
                            params={'q': o.venue})
        return self.crawl_venues_assist(resp, o.venue)

    def crawl_publication(self, o):
        """get the bibtex information for a publication."""
        return Publication(o.publ_key)

    def print_parsed_author(self, parsed):
        """print the parsed author information."""
        try:
            for p in parsed:
                self.log.debug("\nName: {n}".format(n=p.name))
                self.log.debug("urlpt: {u}".format(u=p.urlpt))
                self.log.debug("Number of Publications: {pp}".format(
                    pp=len(p.publications)))
                self.log.debug("Home Page: {hp}".format(hp=p.homepages))
                self.log.debug("One Publications: {ppt}".format(
                    ppt=p.publications[0].title))
        except:
            self.log.debug("No results and cannot be printed out.")

    def print_parsed_coauthor(self, parsed):
        """print the coauthor information of a given author."""
        try:
            for p in parsed:
                self.log.debug("\nAuthor information: {pa}".format(
                    pa=p.author))
                self.log.debug("\nCoauthor information: {pc}".format(
                    pc=p.coauthors))
        except:
            self.log.debug("No results and cannot be printed out.")

    def print_parsed_venues(self, parsed):
        """print the paper of a given conference/journal."""
        try:
            for p in parsed:
                self.log.debug("\nVenue Name: {pv}".format(pv=p.venue_name))
                self.log.debug("Venue root url: {pvu}".format(pvu=p.venue_url))
                self.log.debug("\nOne publications (title): {ppt}".format(
                    ppt=p.publications[1].title))
                self.log.debug("\nOne publications (year): {ppy}".format(
                    ppy=p.publications[1].year))
                self.log.debug("\nOne publications (url): {ppu}".format(
                    ppu=p.publications[1].url))
        except:
            self.log.debug("No results and cannot be printed out.")

    def print_parsed_publication(self, parsed):
        """print the bib information of a given publication."""
        try:
            self.log.debug("publications (title): {pt}".format(
                pt=parsed.title))
            self.log.debug("publications (year): {py}".format(py=parsed.year))
            self.log.debug("publications (key): {py}".format(py=parsed.key))
        except:
            self.log.debug("No results and cannot be printed out.")

    def parsing(self, o):
        """parsing the command from terminal input."""
        # initialize the logger
        self.log.info("START THE CRAWLER...")

        if option.mode == 1:
            self.log.info("searching author: {a}".format(a=o.author))
            parsed = self.crawl_author(o)
            self.print_parsed_author(parsed)
        elif option.mode == 2:
            self.log.info(
                "searching the coauthor information of author: {a}".format(
                    a=o.author))
            parsed = self.crawl_coauthor(o)
            self.print_parsed_coauthor(parsed)
        elif option.mode == 3:
            self.log.info("searching the paper of venue: {a}".format(
                     a=o.venue))
            parsed = self.crawl_venues(o)
            self.print_parsed_venues(parsed)
        elif option.mode == 4:
            self.log.info("searching the bib information of the: {a}".format(
                     a=o.publ_key))
            parsed = self.crawl_publication(o)
            self.print_parsed_publication(parsed)
        return parsed

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('--version',
                      dest="version",
                      default=1.0,
                      type="float",
                      )
    parser.add_option("-m",
                      "--mode",
                      dest="mode",
                      default=1,
                      type="int",
                      help="the searching mode.")
    parser.add_option("-a",
                      "--author",
                      dest="author",
                      default="zhenyu wen",
                      type="string",
                      help="the person to search")
    parser.add_option("-v",
                      "--venue",
                      dest="venue",
                      default="nips",
                      type="string",
                      help="get a complete publications of conference/journal")
    parser.add_option("-p",
                      "--publication",
                      dest="publ_key",
                      default="conf/icml/BuloPK16",
                      type="string",
                      help="search the bib information of a publication")
    parser.add_option('-o',
                      '--output',
                      dest='output',
                      action='store_true',
                      default=False,
                      help="Output result or not.")

    (option, args) = parser.parse_args()

    print 'VERSION   :', option.version
    print 'OUTPUT    :', option.output
    print "MODE      :", option.mode
    print 'REMAINING :', args, "\n"

    # parsing
    api = CrawlerAPI()
    parsed = api.parsing(option)
