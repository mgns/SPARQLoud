from handlers.base import BaseHandler
import rdflib
import time
import datetime

import logging
logger = logging.getLogger('boilerplate.' + __name__)

file = "nata.nt"

class FeedListHandler(BaseHandler):
	def get(self):

		queryQuery = "PREFIX wiss: <http://example.org/wiss2014/0.1/> "\
			" SELECT ?feed ?query ?endpoint"\
			" WHERE {?feed wiss:query ?query ; wiss:endpoint ?endpoint . } ORDER BY ?feed"

		#logging.info(query)

		g = rdflib.Graph()
		g.parse(file, format="nt")

		queryQueryRes = g.query(queryQuery)

		feeds = []

		for row in queryQueryRes:
			feed = {
				"feed" : row["feed"].__str__().replace("http://example.org/wiss2014/0.1", "http://localhost:8888"), 
				"query" : row["query"].__str__(),
				"endpoint" : row["endpoint"].__str__()
			}
			feeds.append(feed)
		
		self.render("feedlist.html", feeds=feeds)