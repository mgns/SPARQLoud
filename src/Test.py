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
        ResultRows = qres[0]

    return ResultRows

