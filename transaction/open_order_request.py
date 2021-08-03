"""
module with class which call server for open orders in Order Book
"""
from base.message import Message
import datetime as dt
import numpy as np
from constant import side_type, tif_type, symbol_enum


send_msg = {
	"msg1": "e",
	"UpdateType": 2
}

response_oes_msg = {
	"msg1": "T",
	"MessageType": 31,
	"UserName": "BOU7",
	"Account": 100700,
	"SymbolEnum": 11021,
	"BTCEquity": 100.0,
	"USDTEquity": 10000000.0,
	"FLYEquity": 50000000.0,
	"USDEquity": 10000000.0,
	"ETHEquity": 2000.0,
	"TradingSessionID": 506,
	"LastSeqNum": 20101010,
	"SendingTime": 1624821404365664367
}


class OpenOrderRequest(Message):

	def __init__(self):
		"""
		class for open orders request from server
		"""
		super(OpenOrderRequest, self).__init__()

		self.send_data = send_msg
		self.receive_data = response_oes_msg

	def set_logon_values(self, logonObj) -> None:
		"""
		setting data corresponding logon parameters for given session
		:param logonObj:
		:return:
		"""
		self.send_data['Account'] = logonObj.receive_data['Account']
		self.send_data['SendingTime'] = int(dt.datetime.utcnow().timestamp() * 1e9)
		self.send_data['OrderID'] = np.random.randint(1, 100000000)
		self.send_data['Key'] = logonObj.receive_data['Key']
		self.send_data['MsgSeqID'] = 0
		self.send_data['TradingSessionID'] = logonObj.receive_data['TradingSessionID']

	def set(self, data: dict) -> None:
		"""
		needs to set symbol for which we are calling open orders
		:param data:
		:return:
		"""
		symbol = data['BOSymbol']
		if symbol in symbol_enum.DICT.keys():
			self.send_data['SymbolEnum'] = symbol_enum.DICT[symbol]
		else:
			raise Exception(f'{symbol} is not in allowed symbol. Valid symbols:', symbol_enum.DICT.keys())


def create_open_order_request():
	"""
	creating message
	:return:
	"""
	message = OpenOrderRequest()

	return message
