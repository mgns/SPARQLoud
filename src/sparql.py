from SPARQLWrapper import SPARQLWrapper

import logging
logger = logging.getLogger('boilerplate.' + __name__)


def query(endpoint, query):
	sparql = SPARQLWrapper(endpoint)
	sparql.setQuery(query)
	#sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	
	for result in results["results"]["bindings"]:
	    print(result["label"]["value"])