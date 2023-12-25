from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Schema
from ultipa.structs import DBType
from ultipa.types import ULTIPA, ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList

BOOL_KEYS = ["index", "lte"]
REPLACE_KEYS = {
	"name": "schemaName",
	"type": "propertyType",
}


class SchemaExtra(BaseExtra):
	'''
		Prcessing class that defines settings for schema related operations.
	'''

	def createSchema(self, schema: Schema,
					 requestConfig: RequestConfig = RequestConfig())->ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a schema.

		Args:
			schema: An object of Schema class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''


		command = schema.DBType == DBType.DBNODE and CommandList.createNodeSchema or CommandList.createEdgeSchema
		commandP = [f"`{schema.name}`"]
		if schema.description:
			commandP.append(schema.description)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def listSchema(self, dbType: DBType = None, schemaName: str = None,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		List schema(s).

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE), show both types of schemas by default

			schemaName: The name of designated schema, or show all schemas by default

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		return self.showSchema(dbType, schemaName, requestConfig)

	def showSchema(self, dbType: DBType = None, schemaName: str = None,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Show schema(s).

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE), show both types of schemas by default

			schemaName: The name of designated schema, or show all schemas by default
			
			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		if dbType != None:
			if dbType == DBType.DBNODE:
				command = CommandList.showNodeSchema
			elif dbType == DBType.DBEDGE:
				command = CommandList.showEdgeSchema
			else:
				command = CommandList.showSchema

			if schemaName:
				commandP = '@' + schemaName
			else:
				commandP = ''
		else:
			command = CommandList.showSchema
			commandP = ''

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterSchema(self, dbType: DBType, schemaName: str, newSchemaName: str, description: str = None,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter schema.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			newSchemaName: The new name of schema

			description: The new description of schema

			requestConfig: An object of RequestConfig class

		Returns:
			 UltipaResponse

		'''
		command = dbType == DBType.DBNODE and CommandList.alterNodeSchema or CommandList.alterEdgeSchema
		commandP = '@' + schemaName
		update_dict = {}
		if newSchemaName:
			update_dict.setdefault('name', newSchemaName)
		if description:
			update_dict.update({'description': description})
		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		uqlMaker.addParam("set", update_dict)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropSchema(self, dbType: DBType, schemaName: str,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop schema.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			requestConfig: An object of RequestConfig class

		Returns:
			 UltipaResponse

		'''

		command = dbType == DBType.DBNODE and CommandList.dropNodeSchema or CommandList.dropEdgeSchema
		commandP = '@' + schemaName

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
