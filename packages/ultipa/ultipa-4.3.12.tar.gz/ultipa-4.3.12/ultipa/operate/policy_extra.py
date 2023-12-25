from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE, ULTIPA
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.errors import ParameterException
from ultipa.utils.ResposeFormat import ResponseKeyFormat


JSONSTRING_KEYS = ["graphPrivileges", "systemPrivileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class PolicyExtra(BaseExtra):

	'''
		Processing class that defines settings for policy related operations.
	'''

	def showPolicy(self,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListPolicy:
		'''
		Show policy list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponsePolicy

		'''
		uqlMaker = UQLMAKER(command=CommandList.showPolicy, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		return res

	def showPrivilege(self,
					  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListPrivilege:
		'''
		Show privilege list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListPrivilege

		'''

		uqlMaker = UQLMAKER(command=CommandList.showPrivilege, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS))
		return res

	def getPolicy(self, name:str,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponsePolicy:
		'''
		Get a policy.

		Args:
			name: The name of policy

			requestConfig: An object of RequestConfig class

		Returns:
			ResponsePolicy

		'''

		uqlMaker = UQLMAKER(command=CommandList.getPolicy, commonParams=requestConfig)
		uqlMaker.setCommandParams(name)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		if isinstance(res.data, list) and len(res.data) > 0:
			res.data = res.data[0]
		return res

	def createPolicy(self, request: ULTIPA_REQUEST.CreatePolicy,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a policy.

		Args:
			request:  An object of CreatePolicy class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.createPolicy, commonParams=requestConfig)
		paramsP = [request.name]
		if request.graph_privileges:
			paramsP.append(request.graph_privileges)
		else:
			paramsP.append({})
		if request.system_privileges:
			paramsP.append(request.system_privileges)
		else:
			paramsP.append([])
		if request.policies:
			paramsP.append(request.policies)
		else:
			paramsP.append([])
		uqlMaker.setCommandParams(paramsP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def alterPolicy(self, request: ULTIPA_REQUEST.AlterPolicy,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter a policy.

		Args:
			request:  An object of AlterPolicy class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.alterPolicy, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.name)
		params = {}
		if request.system_privileges is not None:
			params.update({"system_privileges": request.system_privileges})
		if request.graph_privileges is not None:
			params.update({"graph_privileges": request.graph_privileges})
		if request.policies is not None:
			params.update({"policies": request.policies})
		uqlMaker.addParam('set', params, notQuotes=True)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropPolicy(self, name:str,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a policy.

		Args:
			name: The name of policy

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.dropPolicy, commonParams=requestConfig)
		uqlMaker.setCommandParams(name)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def grantPolicy(self, request: ULTIPA_REQUEST.GrantPolicy,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Grant privileges and policies to a user.

		Args:
			request:  An object of GrantPolicy class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.grant, commonParams=requestConfig)
		if request.username:
			uqlMaker.setCommandParams(request.username)
		else:
			raise ParameterException(err='username is a required parameter')

		paramsDict = {}
		if request.graph_privileges:
			paramsDict.setdefault('graph_privileges', request.graph_privileges)

		if request.system_privileges:
			paramsDict.setdefault('system_privileges', request.system_privileges)

		if request.policies:
			paramsDict.setdefault('policies', request.policies)
		uqlMaker.addParam('params', paramsDict, notQuotes=True)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def revokePolicy(self, request: ULTIPA_REQUEST.RevokePolicy,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Revoke privileges and policies from a user.

		Args:
			request: An object of RevokePolicy class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.revoke, commonParams=requestConfig)
		if request.username:
			uqlMaker.setCommandParams(request.username)
		else:
			raise ParameterException(err='username is a required parameter')

		paramsDict = {}
		if request.graph_privileges:
			paramsDict.setdefault('graph_privileges', request.graph_privileges)

		if request.system_privileges:
			paramsDict.setdefault('system_privileges', request.system_privileges)

		if request.policies:
			paramsDict.setdefault('policies', request.policies)
		uqlMaker.addParam('params', paramsDict, notQuotes=True)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
