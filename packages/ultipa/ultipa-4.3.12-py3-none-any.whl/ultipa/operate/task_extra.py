from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
import json

from ultipa.utils.convert import convertToAnyObject
from ultipa.utils.ResposeFormat import ResponseKeyFormat


class ALGO_RETURN_TYPE:
	ALGO_RETURN_REALTIME = 1
	ALGO_RETURN_WRITE_BACK = 2
	ALGO_RETURN_VISUALIZATION = 4


class TaskExtra(BaseExtra):
	'''
	Processing class that defines settings for task and process related operations.
	'''

	def top(self,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListTop:
		'''
		Top real-time processes.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListTop

		'''
		uqlMaker = UQLMAKER(command=CommandList.top, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker)
		return res

	def kill(self, id: str = None, all: bool = False,
			 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		'''
		Kill real-time processes.

		Args:
			id: The ID of real-time process

			all: Whether to kill all real-time processes

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
		commonP = []
		if id:
			commonP = id
		if all:
			commonP = '*'
		uqlMaker = UQLMAKER(command=CommandList.kill, commonParams=requestConfig)
		uqlMaker.setCommandParams(commonP)
		res = self.uqlSingle(uqlMaker)
		return res

	def showTask(self, request: ULTIPA_REQUEST.ShowTask,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListTask:
		'''
		Show back-end tasks.

		Args:
			request:  An object of ShowTask class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListTask

		'''

		_jsonKeys = ['taskJson']
		uqlMaker = UQLMAKER(command=CommandList.showTask, commonParams=requestConfig)
		commonP = []
		if request.name and request.status:
			commonP.append(request.name)
			commonP.append(request.status)
		if request.name and not request.status:
			commonP.append(request.name)
			commonP.append('*')
		if not request.name and request.status:
			commonP.append('*')
			commonP.append(request.status)
		if request.id:
			commonP = request.id
		uqlMaker.setCommandParams(commandP=commonP)
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(jsonKeys=_jsonKeys))
		newDatas = []
		if res.data:
			for obj in res.data:
				obj = obj.__dict__
				newData = ULTIPA_RESPONSE.Task()
				taskJson = obj.get("taskJson", {})
				newData.param = json.loads(taskJson.get("param", "{}"))
				newData.result = taskJson.get("result")
				task_info = taskJson.get("task_info", {})

				if task_info.get('status_code'):
					task_info["status_code"] = ULTIPA.TaskStatusString[task_info.get("TASK_STATUS")]
				if task_info.get('engine_cost'):
					task_info["engine_cost"] = task_info.get("writing_start_time", 0) - task_info.get("start_time", 0)

				newData.task_info = convertToAnyObject(task_info)
				return_type_get = int(task_info.get('return_type', 0))
				return_type = ULTIPA_RESPONSE.Return_Type()
				return_type.is_realtime = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_REALTIME else False
				return_type.is_visualization = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_VISUALIZATION else False
				return_type.is_wirte_back = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_WRITE_BACK else False
				newData.task_info.__setattr__('return_type', return_type)
				newDatas.append(newData)
			res.data = newDatas
		return res

	def clearTask(self, request: ULTIPA_REQUEST.ClearTask,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		'''
		Clear back-end tasks.

		Args:
			request:  An object of ClearTask class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''

		uqlMaker = UQLMAKER(command=CommandList.clearTask, commonParams=requestConfig)
		commonP = []
		if request.all:
			commonP.append('*')
		else:

			if request.name and request.status:
				commonP.append(request.name)
				commonP.append(request.status)
			if request.name and not request.status:
				commonP.append(request.name)
				commonP.append('*')
			if not request.name and request.status:
				commonP.append('*')
				commonP.append(request.status)
			if request.id:
				commonP = request.id

		uqlMaker.setCommandParams(commandP=commonP)
		res = self.UqlUpdateSimple(uqlMaker)

		return res

	def stopTask(self, id: str = None, all: bool = False,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		'''
		Stop back-end tasks.

		Args:
			id: The ID of back-end task

			all: Whether to stop all back-end tasks that are computing

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
		uqlMaker = UQLMAKER(command=CommandList.stopTask, commonParams=requestConfig)
		commonP = []
		if all:
			commonP = '*'
		if id:
			commonP = id
		uqlMaker.setCommandParams(commandP=commonP)
		return self.UqlUpdateSimple(uqlMaker)

	def clusterInfo(self,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ClusterInfo:
		'''
		Show cluster information.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ClusterInfo

		'''
		self.refreshRaftLeader(redirectHost='', requestConfig=requestConfig)
		result = []
		if not requestConfig.graphName:
			graphSetName = 'default'
		else:
			graphSetName = requestConfig.graphName
		for peer in self.hostManagerControl.getAllHostStatusInfo(graphSetName):
			info = ULTIPA_RESPONSE.Cluster()
			info.status = peer.status
			info.host = peer.host
			info.isLeader = peer.isLeader
			info.isFollowerReadable = peer.isFollowerReadable
			info.isAlgoExecutable = peer.isAlgoExecutable
			info.isUnset = peer.isUnset
			info.cpuUsage = None
			info.memUsage = None
			if peer.status:
				ret = self.stats(requestConfig=RequestConfig(host=peer.host))
				if ret.status.code == ULTIPA.Code.SUCCESS:
					info.cpuUsage = ret.data.cpuUsage
					info.memUsage = ret.data.memUsage

			result.append(info)
		res = ULTIPA_RESPONSE.Response()
		res.data = result
		return res
