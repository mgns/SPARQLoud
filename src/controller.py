import rdflib, SPARQLWrapper
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
import re, time, hashlib, urllib, datetime, logging
from datetime import datetime
from threading import Timer


#query = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT (COUNT(?s) AS ?c) WHERE { ?s foaf:name ?names }"

uri = "test.nt"
feed_uri = "nata.nt"

total_feed = "PREFIX wiss: <http://example.org/wiss2014/0.1/> SELECT (COUNT(DISTINCT ?s) AS ?c) WHERE {?s a wiss:Feed}"
#check_query = "PREFIX wiss: <http://example.org/wiss2014/0.1/> SELECT (COUNT(DISTINCT ?s) AS ?c) WHERE { ?s wiss:query \"" + query + "\" ; wiss:endpoint \"" + uri + "\".}"

#the controller is triggered by the from and the sheduler
#query -> the query the user wants to execute
#endpoint -> the endpoint against which the user wants to execute the query
def controller(query, uri):
	rs_prior_number = int(0)
	#calls the sparql.py to execute the query and retrieves the new results
	rs_number = sparqlquery(query_rewrite(query), uri)
	print("current number " + str(rs_number))

	#checks if the feed is already in the data.ttl
	check_query = "PREFIX wiss: <http://example.org/wiss2014/0.1/> SELECT (COUNT(DISTINCT ?s) AS ?c) WHERE { ?s wiss:query \"" + query + "\" ; wiss:endpoint \"" + uri + "\".}"
	check_query_num = sparqlquery(check_query, feed_uri)
	print("check query number " + str(check_query_num))

	if int(check_query_num) == int(0):
		print("stores new query " + query)
		store(query, uri, rs_number)
	else:
#		print "compares with the registry"
		#if yes retrieves the existing number and compares
		rs_prior_number = getResultSizeSet(query, uri)
#		print "prior number " + str(rs_prior_number)

		if(int(rs_number) != int(rs_prior_number)):
			store(query, uri, rs_number)
#			print "notification sent"
		#send notification

#rewrites the query to write the results
def query_rewrite(query):
	count_query = re.sub(r"SELECT ([^{])+", r"SELECT (COUNT(*) AS ?c) WHERE ", query, flags=re.I)
	print("rewrite query to " + count_query)
	return count_query

#executes the query and gets the number of current rows
def sparqlquery(Query ,DataSetDescriptor):
 
    g = rdflib.Graph()
    if DataSetDescriptor[0] == "h" :
        sparql = SPARQLWrapper.SPARQLWrapper(DataSetDescriptor)
        sparql.setQuery(Query)
        sparql.setReturnFormat(SPARQLWrapper.JSON)
        qres = sparql.query().convert()
        for result in qres["results"]["bindings"]:
            ResultRows = result["c"]["value"]
        # g.parse(DataSetDescriptor)
    else :
    	#print Query
        g.parse(DataSetDescriptor, format= rdflib.util.guess_format(DataSetDescriptor))
        qres = g.query(Query)
        for row in qres.result : res = row
        ResultRows = res[0]
 
    return ResultRows

def store(query, uri, resultSetSize):
	WISS = Namespace("http://example.org/wiss2014/0.1/")
	XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

	g = rdflib.Graph()
	g.parse("nata.nt", format="nt")

	qidString = str(uri + "?query=" + query) #urllib.parse.quote(query))

	m = hashlib.md5()
	m.update(qidString.encode('utf-8'))
	qidHash = m.hexdigest()
	timeStamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')

	bnode = BNode()

	g.add( (WISS['feed/Q' + str(qidHash)], WISS['query' ], Literal(query)) )
	g.add( (WISS['feed/Q' + str(qidHash)], WISS['endpoint' ], Literal(uri)) )
	g.add( (WISS['feed/Q' + str(qidHash)], WISS['feed' ], bnode ) )

	g.add( (bnode, WISS['resultSetSize' ], Literal(resultSetSize)) )
	g.add( (bnode, WISS['lastExecuted' ], Literal(timeStamp)) )

	g.serialize(destination='nata.nt', format='nt')

def get_feed(query, uri):
	num = getResultSizeSet(query, uri)
	return num


def getResultSizeSet(query, uri):
	logger = logging.getLogger('boilerplate.' + __name__)

	result_query = "SELECT DISTINCT ?result ?executed "\
		"WHERE { "\
		   "?f <http://example.org/wiss2014/0.1/endpoint> \"" + uri + "\" ; "\
      		  "<http://example.org/wiss2014/0.1/query> \"" + query + "\" ; "\
      		  "<http://example.org/wiss2014/0.1/feed> ?bn . "\
    	   "?bn <http://example.org/wiss2014/0.1/resultSetSize> ?result ; "\
      		  "<http://example.org/wiss2014/0.1/lastExecuted> ?executed . "\
	"} "\
	" ORDER BY DESC(?executed) "\
	" LIMIT 1" 

	g = rdflib.Graph()
	g.parse(feed_uri, format="nt")

	results = []
	res = []

	qres = g.query(result_query)

	for row in qres :
		logger.info(row)
		res = {"result" : row["result"], "executed" : row["executed"]}

	if(len(res) > int(0)):
		return res["result"]

def getQueries():
    query = " SELECT ?feed ?query ?endpoint ?result"\
    " WHERE {"\
    " ?feed <http://example.org/wiss2014/0.1/query> ?query ;"\
    "       <http://example.org/wiss2014/0.1/endpoint> ?endpoint ;"\
    "       <http://example.org/wiss2014/0.1/resultSetSize> ?result ;"\
    "       <http://example.org/wiss2014/0.1/lastExecuted> ?executed . }"
 #   print "query " + query
 
    g = rdflib.Graph()
    g.parse(feed_uri, format="nt")
 
    results = []
 
    qres = g.query(query)
    for row in qres :
        logger.info(row)
        result = {"qid" : row["feed"], "query" : row["query"], "endpoint" : row["endpoint"], "result" : row["result"]}
        results.append(result)

 #   print results

    return results


def CheckUpdates ():
    Timer(10,check_updates, ()).start()
    return 0

def check_updates ():
	getQueries()
#	print "oti nanai \n"

#controller(query, uri)
#CheckUpdates ()