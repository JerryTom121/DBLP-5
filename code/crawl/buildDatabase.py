# -*- coding: utf-8 -*-
"""Build the database for the crawler system."""

from pymongo import MongoClient, ASCENDING
from utils import parameters as params


def init_collection():
    """initialize one of the collections of the mongodb."""
    client = MongoClient(params.DATABASE_LOCATION, params.DATABASE_PORT)
    db = client.crawl
    authors = db.authors
    publications = db.publications
    if params.DATABASE_MODE:
        destroy_collection(authors)
        destroy_collection(publications)
    authors.create_index([("urlpt", ASCENDING)], unique=True)
    publications.create_index([("key", ASCENDING)], unique=True)
    return authors, publications


def destroy_collection(collection):
    """a helper function to destory the collection of the db."""
    collection.drop()
