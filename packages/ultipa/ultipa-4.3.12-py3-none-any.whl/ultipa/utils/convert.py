import json
from typing import List

from ultipa.structs.BaseModel import BaseModel


class Any(BaseModel):
	'''
	Any model
	'''
	def __str__(self):
		return str(self.__dict__)

	pass


def convertToAnyObject(dict1: dict):
	'''
	Convert Dict to Object.

	Args:
		dict1:

	Returns:

	'''
	obj = Any()
	for k in dict1.keys():
		v = dict1[k]
		if isinstance(v, list):
			for i, n in enumerate(v):
				if isinstance(n, dict):
					v[i] = convertToAnyObject(n)
		# if isinstance(v, dict):
		#     v = convertToAnyObject(v)
		obj.__setattr__(k, v)
	return obj


def convertToListAnyObject(list1: List[dict]):
	'''
	Convert List[Dict] to Object.

	Args:
		list1:

	Returns:

	'''
	if not list1 and isinstance(list1, list):
		return list1
	if not list1:
		return
	newList = []
	for dict1 in list1:
		newList.append(convertToAnyObject(dict1))
	return newList


def convertTableToDict(table_rows, headers):
	'''
	Convert Table to Object.

	Args:
		table_rows:
		headers:

	Returns:

	'''
	newList = []
	for data in table_rows:
		dic = {}
		for index, header in enumerate(headers):
			dic.update({header.get("property_name"): data[index]})
		newList.append(dic)
	return newList
