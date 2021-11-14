"""
This module generate description of messages as well as valided messages
"""
from constant import (attribute_type,
					  logon_type,
					  message_type,
					  order_message_type,
					  order_type,
					  reject_code,
					  side_type,
					  symbol_enum,
					  tif_type,
					  request_message_type,
					  general_message)

from enum import Enum

MAX_LAYERS = 10
MAX_ORDER = 100


class ConstantDefinitions:
	"""
	general class for constant management
	"""

	def __init__(self, import_type):
		self.type = import_type
		self._dict_def()

	def _dict_def(self):
		self._dict = {k: mt for k, mt in self.type.__dict__.items() if
				not k.startswith('_')}
		self._desc_dict = {mt: k for k, mt in self.type.__dict__.items() if
				   not k.startswith('_')}

	def get_description(self, msg_type: int) -> str:
		try:
			return self._desc_dict[msg_type]
		except Exception as ex:
			return "KEY_INVALID"

	def is_valid(self, msg_type: int):
		return msg_type in self.list()

	def list(self):
		return self._dict.values()

	def __getitem__(self, item):
		return self._dict[item]

	def __len__(self):
		return len(self._dict)

	def __str__(self):
		return '\n'.join([str(k) + '\t' + self.get_description(k) for k in self.list()])


attribute = ConstantDefinitions(attribute_type)
logon = ConstantDefinitions(logon_type)
message = ConstantDefinitions(message_type)
order_message = ConstantDefinitions(order_message_type)
order = ConstantDefinitions(order_type)
reject = ConstantDefinitions(reject_code)
side = ConstantDefinitions(side_type)

#TODO Symbols can be added in future, so this cannot be as constant
symbol = ConstantDefinitions(symbol_enum)
tif = ConstantDefinitions(tif_type)
request_message = ConstantDefinitions(request_message_type)
general = ConstantDefinitions(general_message)


def set_attributes(*attr) -> str:
	"""
	generates string with attributes
	:param attr: list of int
	:return: string
	"""
	ret = ''.join(['N'] * len(attribute))

	for a in attr:
		if attribute.is_valid(a):
			ret2 = ret[:a] + 'Y'
			if a < len(attribute) - 1:
				ret2 += ret[a+1:]
			ret = ret2[:]
		else:
			raise Exception(f'Attributes not valid. Allowed attributes {attribute.list()}')

	return ret


def get_attributes_desc(attr_str: str) -> list:
	"""
	get description to attributes
	:param attr_str: str
	:return: list of int
	"""
	ret = []
	for i, a in enumerate(attr_str):
		if a == 'Y':
			ret.append(attribute.get_description(i))

	return ret


def validate_attributes(attr_str: str, **msg_cls) -> bool:

	for a in attr_str:
		if a not in ['N', 'Y']:
			return False

	# if len(**msg_cls) > 0:
	# 	ds = attr_str[attribute_type.DISPLY_TYPE]
	# 	if ds == "Y":
	# 		if attr_str[attribute_type.SIZEINCREMENT_TYPE] <= 0:
	# 			cls.RejectReason = reject_code.DISPLAY_SIZE_INVALID
	#
	# 	elif self.RejectReason <= 0:
	# 		self.RejectReason = reject_code.REFRESH_SIZE_INVALID

	return True