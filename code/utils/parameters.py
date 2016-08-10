"""Define the global parameters of crawler."""
DBLP_BASE_URL = 'http://dblp.uni-trier.de/'

DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'
DBLP_VENUES_SEARCH_URL = DBLP_BASE_URL + 'search/venue'

DBLP_PERSON_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_COAUTHORS_URL = DBLP_BASE_URL + 'pers/xc/{urlpt}'
DBLP_RECORDS_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'
