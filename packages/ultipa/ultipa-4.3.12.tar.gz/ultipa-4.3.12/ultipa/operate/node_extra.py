from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig

class NodeExtra(BaseExtra):
	'''
	Processing class that defines settings for node related operations.

	'''
	def searchNode(self, request: ULTIPA_REQUEST.SearchNode,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSearchNode:
		'''
		Query for nodes.

		Args:
			request: An object of SearchNode class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSearchNode

		'''

		uqlMaker = UQLMAKER(command=CommandList.nodes, commonParams=requestConfig)
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

	def insertNode(self, request: ULTIPA_REQUEST.InsertNode,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseInsert:
		'''
		Insert nodes.

		Args:
			request: An object of InsertNode class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.insert, commonParams=requestConfig)
		if request.upsert:
			uqlMaker = UQLMAKER(command=CommandList.upsert, commonParams=requestConfig)
		if request.overwrite:
			uqlMaker.addParam('overwrite', "", required=False)
		if request.schemaName:
			uqlMaker.addParam('into', request.schemaName, required=False)

		uqlMaker.addParam('nodes', request.nodes)

		if request.isReturnID:
			uqlMaker.addParam('as', "nodes")
			uqlMaker.addParam('return', "nodes._uuid")

		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res
		if request.isReturnID:
			if len(res.aliases) > 0:
				res.data = res.items.get(res.aliases[0].alias).data
		return res

	def updateNode(self, request: ULTIPA_REQUEST.UpdateNode,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Update nodes.

		Args:
			request: An object of UpdateNode class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.updateNodes, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		uqlMaker.addParam("set", request.values)
		uqlMaker.addParam("silent", request.silent)
		res = self.uqlSingle(uqlMaker)
		return res

	def deleteNode(self, request: ULTIPA_REQUEST.DeleteNode,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Delete nodes.

		Args:
			request: An object of DeleteNode class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.deleteNodes, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		res = self.uqlSingle(uqlMaker)
		return res
