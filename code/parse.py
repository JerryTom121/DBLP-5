# -*- coding: utf-8 -*-
"""parse the crawled publication."""
import utils.opfiles as op
from parse import ParsePublications


def main(path_root):
    """the entry."""
    parse_publication = ParsePublications(path_root)
    unique_authors = parse_publication.parse()
    op.write_pickle(unique_authors, "authors_to_download")


if __name__ == '__main__':
    path_root = "./"
    main(path_root)
