from base.message import Message
import datetime as dt
import numpy as np
from constant import symbol_enum


send_msg = {
	"msg1": "Y",
	"MessageType": 22,
	"Account": 100700,
	"SymbolName": "BTCUSD",
	"UserName": "BOU7",
	"SymbolEnum": 4,
	"TradingSessionID": 506,
	"Key": 123456,
	"MsgSeqID": 500,
	"SendingTime": 1624859180169634284
}

response_oes_msg = {
	"msg1": "Q",
	"MessageType": "21",
	"SymbolName": "USDUSDT",
	"SymbolEnum": 4,
	"SymbolType": 1,
	"PriceIncrement": 0.5,
	"MaxSize": 5000.0,
	"MinSize": 0.00001,
	"SendingTime": 1624863069122199720,
	"LastSeqNum": 505
}


class InstrumentRequest(Message):

	def __init__(self):
		super(InstrumentRequest, self).__init__()

		self.send_data = send_msg
		self.receive_data = response_oes_msg

	def set_logon_values(self, logonObj):

		self.send_data['Account'] = logonObj.receive_data['Account']
		self.send_data['UserName'] = logonObj.receive_data['UserName']
		self.send_data['SendingTime'] = int(dt.datetime.utcnow().timestamp() * 1e9)
		self.send_data['OrderID'] = np.random.randint(1, 100000000)
		self.send_data['Key'] = logonObj.receive_data['Key']
		self.send_data['MsgSeqID'] = 0
		self.send_data['TradingSessionID'] = logonObj.receive_data['TradingSessionID']

	def set(self, data):
		symbol = data['BOSymbol']
		if symbol in symbol_enum.DICT.keys():
			self.send_data['SymbolEnum'] = symbol_enum.DICT[symbol]
		else:
			raise Exception(f'{symbol} is not in allowed symbol. Valid symbols:', symbol_enum.DICT.keys())


def create_instrument_request():
	message = InstrumentRequest()

	return message
