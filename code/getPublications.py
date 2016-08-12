# -*- coding: utf-8 -*-
"""My crawler to automatically download the information."""

import time
import requests
from os.path import join

from crawlerAPI import CrawlerAPI
from crawl import buildDatabase as builddb
from crawl import auxiliary as auxi
from utils import Logger
from utils import parameters as params
from utils import opfiles as op


class GetPublications(object):

    """a class used to get a list of publications based on given venues."""

    def __init__(self):
        """init."""
        self.log = Logger.get_logger("get_publications")
        self.api = CrawlerAPI()

    def read_list_to_download(self, path):
        """get the list to crawl."""
        data = op.read_txt(path)
        return data

    def crawl_venues(self, venue):
        """crawl the publications of venue."""
        resp = requests.get(params.DBLP_VENUES_SEARCH_URL,
                            params={'q': venue})
        return self.api.crawl_venues_assist(resp, venue)

    def insert_to_db(self, data, db):
        """insert the data to the db."""
        try:
            db.insert_one(data)
        except:
            self.log.warning("already exist in the db.")
            pass

    def parsing_crawled_publications(self, crawled, db, path_record):
        """parsing the crawled publications."""
        for c in crawled:
            self.log.debug("parsing {n}, its url={u}".format(n=c.venue_name,
                           u=c.venue_url))
            total_publications = len(c.publications)
            for ind, publication in enumerate(c.publications):
                if db.find({"key": publication.key}).count() > 0:
                    op.write_to_txt(publication.key + "\tExisted.\n",
                                    path_record, "a")
                    continue
                if len(publication.authors) == 0:
                    continue
                data = {
                    "venue_name": c.venue_name,
                    "acronym": c.acronym,
                    "key": publication.key,
                    "url": params.DBLP_RECORDS_URL.format(key=publication.key),
                    "title": publication.title,
                    "year":  publication.year,
                    "crossref": publication.crossref,
                    "citations": publication.citations,
                    "authors": publication.authors
                }
                self.insert_to_db(data, db)
                op.write_to_txt(
                    publication.key + "\tAdded.\n", path_record, "a")
                if ind % 50 == 0:
                    self.log.info(
                        "parsed {i} publications, existing {t}".format(
                            i=ind, t=total_publications))
                # add time delay to avoid the blocking.
                time_to_sleep = auxi.random_sleep()
                time.sleep(time_to_sleep)

    def start_crawler(self, path_code):
        """start my crawler."""
        # init pathes
        path_list_to_crawl = join(path_code, "list_to_download")
        path_crawler_record = join(path_code, "list_of_downloaded")
        # init logger
        log = Logger.get_logger('crawl_publication')
        log.info("START THE CRAWLER...")
        # init mongodb
        authors, publications = builddb.init_collection()

        # get the venues to crawl.
        venues_to_crawl = self.read_list_to_download(path_list_to_crawl)
        # start the crawler
        for venue in venues_to_crawl:
            venue = venue.strip()
            log.info("crawl the venue named {v}".format(v=venue))
            crawled = self.crawl_venues(venue)
            self.parsing_crawled_publications(crawled, publications,
                                              path_crawler_record)

if __name__ == '__main__':
    path_code = "."
    get_publications = GetPublications()
    get_publications.start_crawler(path_code)
