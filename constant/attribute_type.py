RESERVED_TYPE = 0
HIDDEN_TYPE = 1
DISPLY_TYPE = 2
SIZEINCREMENT_TYPE = 3
POST_TYPE = 4
PRICEINCREMENT_TYPE = 5
OFFSET_TYPE = 6
STOP_MKT_TYPE = 7
STOP_LMT_TYPE = 8
PEG_TYPE = 9
TSL_TYPE = 10
TSM_TYPE = 11

from constant import attribute_type as module_self

DICT = {k: mt for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self')}
INVDICT = {mt: k for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self') and k != 'DICT'}


def get_attributes(*attr) -> str:

	ret = ''
	for k, v in INVDICT.items():
		ret += 'N'

	for a in attr:
		if isinstance(a, int):
			if a in INVDICT.keys():
				ret2 = ret[:a] + 'Y'
				if a < len(DICT) - 1:
					ret2 += ret[a+1:]
				ret = ret2[:]
			else:
				raise Exception(f'Attributes not valid. Allowed attributes {INVDICT.keys()}')
		else:
			raise Exception(f'Atributes should be integers. Found {type(a)}')

	return ret


def get_attributes_desc(attr_str: str) -> list:

	ret = []
	for i, a in enumerate(attr_str):
		if a == 'Y':
			ret.append(INVDICT[i])

	return ret