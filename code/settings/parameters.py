"""Define the global parameters of crawler."""
DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_BASE_API_URL = 'http://dblp.dagstuhl.de/search/venue/api'

DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author/api'
DBLP_PUBLICATION_SEARCH_URL = DBLP_BASE_URL + 'search/publ/api'
DBLP_VENUES_SEARCH_URL = DBLP_BASE_API_URL + 'search/venues'


DBLP_PERSON_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_COAUTHORS_URL = DBLP_BASE_URL + 'pers/xc/{urlpt}'
DBLP_RECORDS_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'


DOWNLOAD_DELAY = 4
DATABASE_LOCATION = "mongodb"
DATABASE_PORT = 27017

# normally it should be False otherwise we will lose information
DATABASE_MODE = False
