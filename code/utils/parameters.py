"""Define the global parameters of crawler."""
DBLP_BASE_URL = 'http://dblp.uni-trier.de/'

DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'


DBLP_PERSON_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_PUBLICATION_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'
DBLP_VENUES_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'
