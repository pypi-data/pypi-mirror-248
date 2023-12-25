from ultipa.operate.base_extra import BaseExtra

from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig

class EdgeExtra(BaseExtra):
	'''
	Processing class that defines settings for edge related operations.

	'''

	def searchEdge(self, request: ULTIPA_REQUEST.SearchEdge,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSearchEdge:
		'''
		Query for edges.

		Args:
			request: An object of SearchEdge class 

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSearchEdge

		'''

		uqlMaker = UQLMAKER(command=CommandList.edges, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)

		uqlMaker.addParam('as', request.select.aliasName)
		uqlMaker.addParam("return", request.select)

		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res
		return res

	def insertEdge(self, request: ULTIPA_REQUEST.InsertEdge,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseInsert:
		'''
		Insert edges.

		Args:
			request: An object of InsertEdge class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseInsert
		'''

		uqlMaker = UQLMAKER(command=CommandList.insert, commonParams=requestConfig)
		if request.upsert:
			uqlMaker = UQLMAKER(command=CommandList.upsert, commonParams=requestConfig)
		if request.overwrite:
			uqlMaker.addParam('overwrite', "", required=False)
		if request.schemaName:
			uqlMaker.addParam('into', request.schemaName, required=False)
		uqlMaker.addParam('edges', request.edges)

		if request.isReturnID:
			uqlMaker.addParam('as', "edges")
			uqlMaker.addParam('return', "edges._uuid")
		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res
		if request.isReturnID:
			if len(res.aliases) > 0:
				res.data = res.items.get(res.aliases[0].alias).data
		return res

	def updateEdge(self, request: ULTIPA_REQUEST.UpdateEdge,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Update edges.

		Args:
			request: An object of UpdateEdge class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.updateEdges, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		uqlMaker.addParam("set", request.values)
		uqlMaker.addParam("silent", request.silent)
		res = self.UqlUpdateSimple(uqlMaker)
		return res

	def deleteEdge(self, request: ULTIPA_REQUEST.DeleteEdge,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Delete edges.

		Args:
			request: An object of DeleteEdge class
			
			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.deleteEdges, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		res = self.UqlUpdateSimple(uqlMaker)
		return res
