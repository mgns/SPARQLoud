import rdflib
import urllib
import time
import datetime
import hashlib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import Namespace

import logging
logger = logging.getLogger('boilerplate.' + __name__)

WISS = Namespace("http://example.org/wiss2014/0.1/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

file = "data.nt"
	
def store(query, endpoint, resultSetSize):

	g = rdflib.Graph()
	g.parse(file, format="nt")

	timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
	qidString = str(endpoint + "?query=" + urllib.parse.quote(query))
	#qidHash = hashlib.md5(qidString.encode('utf-8')).hexdigest

	m = hashlib.md5()
	m.update(qidString.encode('utf-8'))
	qidHash = m.hexdigest()

	g.add( (WISS['feed/Q' + str(qidHash)], WISS['query'], Literal(query)) )
	g.add( (WISS['feed/Q' + str(qidHash)], WISS['endpoint'], Literal(endpoint)) )
	g.add( (WISS['feed/Q' + str(qidHash)], WISS['resultSetSize'], Literal(resultSetSize)) )
	g.add( (WISS['feed/Q' + str(qidHash)], WISS['lastExecuted'], Literal(timeStamp)) )

	g.serialize(destination=file, format='nt')

def getQueries():
	query = " SELECT ?feed ?query ?endpoint ?result"\
	" WHERE {"\
	" ?feed <http://example.org/wiss2014/0.1/query> ?query ;"\
	"       <http://example.org/wiss2014/0.1/endpoint> ?endpoint ;"\
	"       <http://example.org/wiss2014/0.1/resultSetSize> ?result ;"\
	"       <http://example.org/wiss2014/0.1/lastExecuted> ?executed . }"

	g = rdflib.Graph()
	g.parse(file, format="nt")

	results = []

	qres = g.query(query)
	for row in qres :
		logger.info(row)
		result = {"qid" : row["feed"], "query" : row["query"], "endpoint" : row["endpoint"], "result" : row["result"]}
		results.append(result)

	return results

#store ("SELECT ?a WHERE {?a a <http://dbpedia.org/ontology/Person> .}", "http://dbpedia.org/sparql", 23)

#results = getQueries()
#for row in results : print(row["query"])
