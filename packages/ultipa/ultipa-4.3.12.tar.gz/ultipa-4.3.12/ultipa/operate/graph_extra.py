import time

import json

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Graph
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat

REPLACE_KEYS = {
	"graph": "name",
}


class GraphExtra(BaseExtra):

	'''
	Processing class that defines settings for graphset related operations.
	'''

	def uqlCreateSubgraph(self, uql: str, subGraphName: str, requestConfig: RequestConfig = RequestConfig()):
		ret = self.uql(uql, requestConfig)
		graphRet = self.getGraph(subGraphName)
		if graphRet.status.code != 0:
			self.createGraph(Graph(name=subGraphName))
			time.sleep(3)


	def listGraph(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListGraph:
		'''
		Acquire graphset list (for internal use).

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListGraph
		'''

		return self.showGraph(requestConfig)

	def showGraph(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListGraph:
		'''
		Acquire graphset list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListGraph
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams("")
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		return res

	def getGraph(self, graphName: str,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseGraph:
		'''
		Acquire a designated graphset.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)

		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		if isinstance(res.data, list) and len(res.data) > 0:
			res.data = res.data[0]
		return res

	def createGraph(self, graph: Graph,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a graphset.

		Args:
			grpah: An object of Graph class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.createGraph, commonParams=requestConfig)
		if graph.description:
			uqlMaker.setCommandParams([graph.name, graph.description])
		else:
			uqlMaker.setCommandParams(graph.name)
		res = self.uqlSingle(uqlMaker)
		return res

	def dropGraph(self, graphName: str,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a graphset.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.dropGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterGraph(self, oldGraphName: str, newGraphName: str, newDescription: str = None,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter a graphset

		Args:
			oldGraphName: The orignal name of graphset

			newGraphName: The new name of graphset

			newDescription: The new description of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		requestConfig.graphName = oldGraphName
		uqlMaker = UQLMAKER(command=CommandList.alterGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(oldGraphName)
		data = {"name": newGraphName}
		if newDescription is not None:
			data.update({'description': newDescription})
		uqlMaker.addParam("set", data)
		res = self.uqlSingle(uqlMaker)
		return res
