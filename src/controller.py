import rdflib, SPARQLWrapper
import re

query = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT (COUNT(?s) AS ?c) WHERE { ?s foaf:name ?names }"

uri = "test.n3"
uri2 = "data.ttl"
total_feed = "SELECT (COUNT(DISTINCT ?s) AS ?c) WHERE {?s a wiss:Feed}"
check_query = "PREFIX wiss: <http://example.org> SELECT (COUNT(DISTINCT ?s) AS ?c) WHERE { ?s a wiss:Feed ; wiss:query \"" + query + "\" ; wiss:endpoint \"" + uri + "\".}"

#the controller is triggered by the from and the sheduler
#query -> the query the user wants to execute
#endpoint -> the endpoint against which the user wants to execute the query
def controller(query, uri):
	#
	#gets the query and rewrites it
	#query re-writing
	#count_query = query_rewrite(query)
	#counting rows
	count_query = query

	#calls the sparql.py to execute the query and retrieves the new results
	rs_number = sparqlquery(count_query, uri)
	print("current number " + str(rs_number))

	#checks if the feed is already in the data.ttl
	check_query_num = sparqlquery(check_query, uri2)
	if(check_query_num == 0):
		store(query, uri)
	else:
		#if yes retrieves the existing number and compares
		rs_prior_number = get_feed(query, uri)
		print("prior number " + str(rs_prior_number))

		if(rs_number != rs_prior_number):
			print("notification sent")
		#send notification

#rewrites the query to write the results
def query_rewrite(query):
	count_query = re.sub(r"SELECT ([^{])+", r"SELECT (COUNT(*) AS ?c) WHERE ", query, flags=re.I)
	print(count_query)
	return count_query

#executes the query and gets the number of current rows
import rdflib, SPARQLWrapper

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
		g.parse(DataSetDescriptor, format= rdflib.util.guess_format(DataSetDescriptor))
		qres = g.query(Query)
		for row in qres :
			res = row
		ResultRows = res[0]
 
	return ResultRows

def store(query, uri):
	print("")

def get_feed(query, uri):
	num = sparqlquery(query, uri)
	return 3


controller(query, uri)
