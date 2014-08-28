from handlers.base import BaseHandler
import rdflib
import time
import datetime

import logging
logger = logging.getLogger('boilerplate.' + __name__)

file = "nata.nt"

class FeedHandler(BaseHandler):
	def get(self, path):

		queryQuery = "PREFIX wiss: <http://example.org/wiss2014/0.1/> "\
			" SELECT ?query ?endpoint"\
			" WHERE {<http://example.org/wiss2014/0.1/feed/Q" + path + "> wiss:query ?query ; wiss:endpoint ?endpoint . }"

		queryFeed = "PREFIX wiss: <http://example.org/wiss2014/0.1/> "\
			" SELECT ?result ?time"\
			" WHERE {<http://example.org/wiss2014/0.1/feed/Q" + path + "> wiss:feed ?bn . ?bn wiss:lastExecuted ?time ; wiss:resultSetSize ?result . }"\
			" ORDER BY DESC(?time)"

		#logging.info(query)

		url = "http://localhost:8888/feed/Q" + path
		huburl = "hubtest"

		g = rdflib.Graph()
		g.parse(file, format="nt")

		queryQueryRes = g.query(queryQuery)
		queryFeedRes = g.query(queryFeed)

		query = ''
		endpoint = ''

		for r in queryQueryRes:
			query = r["query"]
			endpoint = r["endpoint"]
			break
		
		answer = '<?xml version="1.0" encoding="UTF-8"?>\n'\
			'<feed xmlns="http://www.w3.org/2005/Atom">\n'\
			'  <title type="text">Query "' + query + '" on endpoint ' + endpoint + '</title>\n'\
			'  <id>' + path + '</id>\n'\
			'  <updated>' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ') + '</updated>\n'\
			'  <author>\n'\
			'    <name>WISS2014</name>\n'\
			'  </author>\n'\
			'  <link rel="self" href="' + url + '" title="WISS2014" type="application/atom+xml"/>\n'\
			'  <link rel="hub" href="' + huburl + '"/>\n'
		for row in queryFeedRes :
			answer = answer + '  <entry>\n'\
				'    <id>' + path + '@' + row["time"] + '</id>\n'\
				'    <title type="text">Update on ' + row["time"] + '</title>\n'\
				'    <content type="text">New result set size is ' + row["result"] + '</content>\n'\
				'    <published>' + row["time"] + '</published>\n'\
				'    <updated>' + row["time"] + '</updated>\n'\
				'  </entry>\n';
		answer = answer + '</feed>'

		self.set_header('Content-Type', 'application/atom+xml') # whatever
		#self.write("feed.xml", url="test", huburl="hubtest", date=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), items=feeds)
		self.write(answer)
