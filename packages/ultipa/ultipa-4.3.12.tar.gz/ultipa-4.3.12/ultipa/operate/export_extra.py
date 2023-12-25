from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.configuration.RequestConfig import RequestConfig

class ExportExtra(BaseExtra):
	'''
		Processing class that defines settings for data exporting operation.
	'''

	def export(self, request: ULTIPA_REQUEST.Export,
			   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseExport:
		'''
		Export data.

		Args:
			request: An object of Export class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseExport
		'''
		res = self.exportData(request, requestConfig)
		return res
