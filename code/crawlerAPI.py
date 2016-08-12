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


def crawl_author_assist(resp):
    """an assistant function to help the function 'crawl_author'."""
    parsed = []
    root = etree.fromstring(resp.content)
    # print(etree.tostring(root, pretty_print=True))
    for urlpt in root.xpath('/authors/author/@urlpt'):
        parsed.append(Author(urlpt))
    return parsed


def crawl_author(o, log):
    """get an author's information in DBLP."""
    resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                        params={'xauthor': o.author})
    return crawl_author_assist(resp)


def crawl_coauthor_assist(resp):
    """an assistant function to help the function 'crawl_coauthor'."""
    parsed = []
    root = etree.fromstring(resp.content)
    for urlpt in root.xpath('/authors/author/@urlpt'):
        parsed.append(CoAuthor(urlpt))
    return parsed


def crawl_coauthor(o, log):
    """get an author's coauthor information in DBLP."""
    resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                        params={'xauthor': o.author})
    return crawl_coauthor_assist(resp)


def crawl_venues_assist(resp, venue, log):
    """an assistant function to help the function 'crawl_venues'."""
    parsed = []
    root = etree.fromstring(resp.content)
    # print(etree.tostring(root, pretty_print=True))
    venues = [{x.tag: x.text for x in hit.xpath('info/*')}
              for hit in root.xpath('//result/hits/hit')]
    venues = [v for v in venues
              if v.get("acronym", "").lower() == venue.lower()]
    log.debug("retrieved venues: {v}".format(v=venues))
    for venue in venues:
        log.info("processing {v}".format(v=venue['venue']))
        parsed.append(Venues(venue))
    return parsed


def crawl_venues(o, log):
    """get the information of a venue (conference/journal) in DBLP."""
    resp = requests.get(params.DBLP_VENUES_SEARCH_URL,
                        params={'q': o.venue})
    return crawl_venues_assist(resp, o.venue, log)


def crawl_publication(o, log):
    """get the bibtex information for a publication."""
    return Publication(o.publ_key)


def print_parsed_author(parsed):
    """print the parsed author information."""
    try:
        for p in parsed:
            print "\nName:", p.name
            print "urlpt:", p.urlpt
            print "Number of Publication:", len(p.publications)
            print "Home Page:", p.homepages
            print "One of the Publications:", p.publications[0].title
    except:
        print "No results and cannot be printed out."


def print_parsed_coauthor(parsed):
    """print the coauthor information of a given author."""
    try:
        for p in parsed:
            print "\nAuthor information:", p.author
            print "\nCoauthor information:", p.coauthors
    except:
        print "No results and cannot be printed out."


def print_parsed_venues(parsed):
    """print the paper of a given conference/journal."""
    try:
        for p in parsed:
            print "\nVenue Name:", p.venue_name
            print "Venue root url:", p.venue_url
            print "\nOne of the publications (title):", p.publications[1].title
            print "\nOne of the publications (year):", p.publications[1].year
            print "\nOne of the publications (url):", p.publications[1].url
    except:
        print "No results and cannot be printed out."


def print_parsed_publication(parsed):
    """print the bib information of a given publication."""
    try:
            print "publications (title):", parsed.title
            print "publications (year):", parsed.year
            print "publications (url):", parsed.url
    except:
        print "No results and cannot be printed out."


def parsing(o):
    """parsing the command from terminal input."""
    # initialize the logger
    log = Logger.get_logger('DBLP_Crawler_API')
    log.info("START THE CRAWLER...")

    if option.mode == 1:
        log.info("searching author: {a}".format(a=o.author))
        parsed = crawl_author(o, log)
        print_parsed_author(parsed)
    elif option.mode == 2:
        log.info("searching the coauthor information of author: {a}".format(
            a=o.author))
        parsed = crawl_coauthor(o, log)
        print_parsed_coauthor(parsed)
    elif option.mode == 3:
        log.info("searching the paper of venue: {a}".format(
                 a=o.venue))
        parsed = crawl_venues(o, log)
        print_parsed_venues(parsed)
    elif option.mode == 4:
        log.info("searching the bib information of the: {a}".format(
                 a=o.publ_key))
        parsed = crawl_publication(o, log)
        print_parsed_publication(parsed)
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
    parsed = parsing(option)
    print "\nThe number of results is: {n}\n".format(n=len(parsed))
