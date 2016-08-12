# -*- coding: utf-8 -*-
"""get the data for a specific conference/journal."""

import time
import requests
from bs4 import BeautifulSoup as BS
from os.path import basename

from utils import Logger
from lazyAPIData import LazyAPIData
from publication import Publication
import auxiliary as auxi


class Venues(LazyAPIData):

    """
    Represents a DBLP venues (conference/journal).
    All data but the author's key is lazily loaded.
    Fields that aren't provided by the underlying XML are None.

    Attributes:
    name - the author's primary name record
    publications - a list of lazy-loaded Publications results by this author
    homepages - a list of author homepage URLs
    homonyms - a list of author aliases
    """

    def __init__(self, venue):
        """initialization."""
        self.venue_name = venue['venue']
        self.venue_url = venue['url']
        self.acronym = venue['acronym']
        self.xml = None
        super(Venues, self).__init__(['publications'])

    def crawl_more_venue_urls(self):
        """using the venue url to get the exact/detailed urls."""
        print("using a venue url to get more detailed venue urls.")
        url_basename = basename(self.venue_url)
        resp = requests.get(self.venue_url)
        html = BS(resp.content, 'lxml')
        html_data = html.findAll("div", {"class": "data"})
        urls = []
        for data in html_data:
            urls += [x['href']
                     for x in data.findAll(href=True)
                     if url_basename in x['href'] and
                     url_basename + "/" + url_basename in x['href']]
        return urls

    def crawl_publication(self, url):
        """crawl the key information for a single publication."""
        print("get the key information of {k}.".format(k=url))
        resp = requests.get(url)
        html = BS(resp.content, 'lxml')
        html_data = html.findAll("li", {"class": "entry"})
        publication_keys = [data['id'] for data in html_data]
        return publication_keys

    def crawl_publications(self, venue_urls):
        """crawl the key information for a list of publications."""
        print("get the publications' key information.")
        publications_urls = []
        for url in venue_urls:
            publications_urls += self.crawl_publication(url)
            time_to_sleep = auxi.random_sleep()
            time.sleep(time_to_sleep)
        return publications_urls

    def load_data(self):
        """load data of the conference."""
        venue_urls = self.crawl_more_venue_urls()
        publications_urls = self.crawl_publications(venue_urls)

        data = {
            "venue urls": venue_urls,
            "publication urls": publications_urls,
            "publications": [Publication(k) for k in publications_urls]
        }
        self.data = data
