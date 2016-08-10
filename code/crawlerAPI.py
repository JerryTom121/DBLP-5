# -*- coding: utf-8 -*-
"""A entry for different functions of the crawler."""

import requests
from lxml import etree
from optparse import OptionParser
from crawl import Author
from crawl import CoAuthor
from utils import Logger
from utils import parameters as params
from utils import opfiles as op


def parsing_author(o, log):
    """parsing an author's information in DBLP."""
    resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                        params={'xauthor': o.author})
    root = etree.fromstring(resp.content)
    return [Author(urlpt)
            for urlpt in root.xpath('/authors/author/@urlpt')]


def parsing_coauthor(o, log):
    """parsing an author's coauthor information in DBLP."""
    resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                        params={'xauthor': o.author})
    root = etree.fromstring(resp.content)
    return [CoAuthor(urlpt)
            for urlpt in root.xpath('/authors/author/@urlpt')]


def print_parsed_author(parsed):
    """print the parsed author information."""
    try:
        for p in parsed:
            print "\nName:", p.name
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


def parsing(o):
    """parsing the command from terminal input."""
    # initialize the logger
    log = Logger.get_logger('DBLP Crawler')
    log.info("START THE CRAWLER...")

    if option.mode == 1:
        log.info("searching author: {a}".format(a=o.author))
        parsed = parsing_author(o, log)
        print_parsed_author(parsed)
    elif option.mode == 2:
        log.info("searching the coauthor information of author: {a}".format(
            a=o.author))
        parsed = parsing_coauthor(o, log)
        print_parsed_coauthor(parsed)
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

    if option.output:
        print "output the crawled data to the current..."
        folder = op.build_result_folder("1470822006")
        print "done!"
    else:
        print "\nThe number of results is: {n}\n".format(n=len(parsed))
