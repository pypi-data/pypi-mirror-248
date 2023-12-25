from ultipa import DBType
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig


class IndexExtra(BaseExtra):

	'''
	Processing class that defines settings for index related operations.
	'''

	def showIndex(self, dbType: DBType = None,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all indice.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE), show both types of indice by default

			requestConfig: An object of RequestConfig class
			
		Returns:
			ResponseListIndex
		'''
		if dbType != None:
			command = dbType == DBType.DBNODE and CommandList.showNodeIndex or CommandList.showEdgeIndex
		else:
			command = CommandList.showIndex
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		return res

	def showFulltext(self, dbType: DBType = None,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListFulltextIndex:
		'''
		Show all full-text indice.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE), show both types of full-text indice by default

			requestConfig: An object of RequestConfig class
		Returns:
			ResponseListFulltextIndex
		'''
		if dbType != None:
			command = dbType == DBType.DBNODE and CommandList.showNodeFulltext or CommandList.showEdgeFulltext
		else:
			command = CommandList.showFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		return res

	def createIndex(self, request: ULTIPA_REQUEST.CreateIndex,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create an index.

		Args:
			request: An object of CreateIndex class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = request.DBtype == DBType.DBNODE and CommandList.createNodeIndex or CommandList.createEdgeIndex
		commandP = request.toString
		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def createFulltext(self, request: ULTIPA_REQUEST.CreateFulltext,
					   rquestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a full-text index.

		Args:
			request: An object of CreateFulltext class

			rquestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		command = request.DBtype == DBType.DBNODE and CommandList.createNodeFulltext or CommandList.createEdgeFulltext
		commandP = [request.toString, request.name]
		uqlMaker = UQLMAKER(command=command, commonParams=rquestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropIndex(self, request: ULTIPA_REQUEST.DropIndex,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop an index.

		Args:
			request: An object of DropIndex class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''
		command = request.DBtype == DBType.DBNODE and CommandList.dropNodeIndex or CommandList.dropEdgeIndex
		commandP = request.toString

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropFulltext(self, request: ULTIPA_REQUEST.DropFulltext,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a full-text index.

		Args:
			request: An object of DropFulltext class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = request.DBtype == DBType.DBNODE and CommandList.dropNodeFulltext or CommandList.dropEdgeFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.fulltextName)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
