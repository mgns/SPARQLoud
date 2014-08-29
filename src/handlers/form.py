from handlers.base import BaseHandler

import controller
import logging
logger = logging.getLogger('boilerplate.' + __name__)


class FormHandler(BaseHandler):
	def get(self):
		logger.info("Called GET")
		self.render("form.html")

	def post(self):
		logger.info("Called POST")
		endpoint = self.get_argument('endpoint')
		query = self.get_argument('query')
		if endpoint == '':
			form_response = "{'error': true, 'msg': 'Please enter an endpoint.'}"
		elif query == '':
			form_response = "{'error': true, 'msg': 'Please enter a query.'}"
		else:
			#sparql.query(endpoint, query)
			#self.write(query)
			controller.controller(query, endpoint)
			form_response = "{'error': false, 'msg': 'Query registered.'}"

		if form_response:
			logger.warning(form_response)

		self.render("form.html")
