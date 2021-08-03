"""
module for creating new order
"""
from base.message import Message
from constant import order_message_type, order_type, side_type, tif_type, symbol_enum, message_type
import datetime as dt
import numpy as np


send_msg = {
	"msg1": "T",
	"MessageType": order_message_type.ORDER_NEW,
	"UpdateType": 2,
}

# Example of response from server
response_oes_msg = {
	"msg1": "T",
	"MessageType": 14,
	"UpdateType": 2,
	"Account": 100700,
	"OrderId": 14333181,
	"SymbolEnum": 4,
	"OrderType": 1,
	"BOPrice": 35040.5,
	"Side": 1,
	"BOOrderQty": 2.0,
	"TIF": 1,
	"DisplaySize": 0.0,
	"RefreshSize": 0.0,
	"BOSymbol": "BTCUSDT",
	"TraderID": "BOU7",
	"SendingTime": 1624781419248402,
	"TradingSessionID": 506,
	"Key": 123456,
	"MsgSeqID": 500
}


class Order(Message):

	def __init__(self):
		super(Order, self).__init__()

		self.send_data = send_msg
		self.receive_data = response_oes_msg
		self.order_names_set = ['BOPrice',
		                        'BOSymbol',
		                        'BOOrderQty',
		                        'BOSide',
		                        'TIF',
		                        'MessageType',
		                        'OrderType',
		                        'OrigOrderID',
		                        'StopLimitPrice',
		                        'Layers',
		                        'SizeIncrement',
		                        'PriceIncrement',
		                        'PriceOffset',
		                        'DisplaySize',
		                        'RefreshSize',
		                        'Attributes']

	def set_logon_values(self, logonObj):
		"""
		set the logon part of parameters
		:param logonObj: ClientLogon
		:return:
		"""
		self.send_data['Account'] = logonObj.receive_data['Account']
		self.send_data['TraderID'] = logonObj.receive_data['UserName']
		self.send_data['SendingTime'] = int(dt.datetime.utcnow().timestamp() * 1e9)
		self.send_data['OrderID'] = np.random.randint(1, 100000000)
		self.send_data['Key'] = logonObj.receive_data['Key']
		self.send_data['MsgSeqID'] = 0
		self.send_data['TradingSessionID'] = logonObj.receive_data['TradingSessionID']

	def _set_param(self, data, par):
		"""
		internal function for seting parameters
		:param data: dict
		:param par: str
		:return:
		"""
		if par in data:
			self.send_data[par] = data[par]
		elif par in self.send_data:
			del self.send_data[par]

	def set(self, data):
		"""
		function which are setting order parameters
		:param data: dict
		:return:
		"""
		list(map(lambda x: self._set_param(data, x), self.order_names_set))

		symbol = data['BOSymbol']
		if symbol in symbol_enum.DICT.keys():
			self.send_data['SymbolEnum'] = symbol_enum.DICT[symbol]
		else:
			raise Exception(f'{symbol} is not in allowed symbol. Valid symbols:', symbol_enum.DICT.keys())


def create_new_order():
	message = Order()

	return message
