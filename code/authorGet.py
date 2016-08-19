# -*- coding: utf-8 -*-
"""My crawler to automatically download the authors' information."""

import time
import requests
from os.path import join

import crawl.buildDatabase as builddb
from crawlerAPI import CrawlerAPI
from utils.logger import Logger
from utils import auxiliary as auxi
import utils.opfiles as op
import settings.parameters as params


class GetAuthors(object):

    """a class used to get a list of publications based on given venues."""

    def __init__(self):
        """init."""
        super(GetAuthors, self).__init__()
        self.log = Logger.get_logger(auxi.get_fullname(self))
        self.api = CrawlerAPI()

    def insert_to_db(self, data, db):
        """insert the data to the db."""
        try:
            db.insert_one(data)
        except:
            self.log.warning("already exist in the db.")
            pass

    def crawl_author(self, author):
        """crawl the publications of author."""
        resp = requests.get(params.DBLP_AUTHOR_SEARCH_URL,
                            params={'xauthor': author})
        return self.api.crawl_author_assist(resp)

    def parsing_crawled_authors(
            self, crawled, db_authors, db_publications, path_record):
        """parsing the crawled authors."""
        for author in crawled:
            self.log.debug("parsing {n}, its url={u}".format(n=author.name,
                           u=author.urlpt))
            if db_publications.find({"urlpt": author.urlpt}).count() > 0:
                op.write_to_txt(author.name + "\t" +
                                author.urlpt + "\tExisted-----------------.\n",
                                path_record, "a")
                continue
            keys = []
            for ind, publication in enumerate(author.publications):
                self.log.debug("processing: {k}".format(k=publication.key))
                if len(publication.authors) == 0:
                    continue
                keys.append(publication.key)
                if db_publications.find({"key": publication.key}).count() > 0:
                    op.write_to_txt(publication.key + "\tExisted.\n",
                                    path_record, "a")
                    continue
                # insert to database
                self.insert_to_db({
                    "key": publication.key,
                    "acronym": publication.key.split('/')[-2],
                    "url": params.DBLP_RECORDS_URL.format(key=publication.key),
                    "title": publication.title,
                    "year":  publication.year,
                    "crossref": publication.crossref,
                    "citations": publication.citations,
                    "authors": publication.authors
                    }, db_publications)
                # add time delay to avoid the blocking.
                time_to_sleep = auxi.random_sleep()
                time.sleep(time_to_sleep)
            # insert to database
            self.insert_to_db({
                    "urlpt": author.urlpt,
                    "name": author.name,
                    "url": params.DBLP_RECORDS_URL.format(key=publication.key),
                    "publication_keys": keys
                }, db_authors)
            op.write_to_txt(author.name + "\t" + author.urlpt +
                            "\tAdded-----------------.\n",
                            path_record, "a")
            time_to_sleep = auxi.random_sleep()
            time.sleep(time_to_sleep)

    def start_crawler(self, path_root):
        """start my crawler."""
        # init pathes
        path_list_to_crawl = join(path_root, "authors_to_download")
        path_crawler_record = join(path_root, "authors_of_downloaded")
        # init logger
        self.log.info("START THE CRAWLER...")
        # init mongodb
        db_authors, db_publications = builddb.init_collection()
        # get the venues to crawl.
        authors = op.load_pickle(path_list_to_crawl)
        # start the crawler
        for ind, author in enumerate(authors):
            self.log.info("crawl the author named: {v}".format(v=author))
            crawled = self.crawl_author(author + "$")
            self.parsing_crawled_authors(
                crawled, db_authors, db_publications, path_crawler_record)
            if ind % 50 == 0:
                self.log.info(
                    "parsed {i}-th author, existing {t}".format(
                        i=ind, t=len(authors)))


if __name__ == '__main__':
    path_root = "."
    get_authors = GetAuthors()
    get_authors.start_crawler(path_root)
