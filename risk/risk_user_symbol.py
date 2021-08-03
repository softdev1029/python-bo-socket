from base.message import Message
import datetime as dt
import numpy as np
from constant import side_type, tif_type, symbol_enum


send_msg = {
	"msg1": "w",
	"MessageType": "w",
	"Account": 100700,
	"SymbolEnum": 4,
	"TradingSessionID": 506,
	"Key": 123456,
	"MsgSeqID": 500,
	"SendingTime": 1624821406361022055
}

response_oes_msg = {
	"MessageType": "N",
	"Account": 100700,
	"SymbolEnum": 1,
	"Leverage": 25.0,
	"LongPosition": 0.0,
	"ShortPostion": 0.0,
	"LongCash": 0.0,
	"ShortCash": 0.0,
	"TradingDisabled": 0,
	"ExecLongCash": 0.0,
	"ExecLongPositon": 0.0,
	"ExecShortCash": 0.0,
	"ExecShortPosition": 0.0,
	"BTCEquity": 100.0,
	"USDTEquity": 10000000.0,
	"ETHEquity": 0.0,
	"USDEquity": 10000000.0,
	"FLYEquity": 0.0,
	"TradingSessionID": 506,
	"LastSeqNum": 200,
	"UpdateType": 2
}


class RiskUserSymbol(Message):
	def __init__(self):
		super(RiskUserSymbol, self).__init__()

		self.send_data = send_msg
		self.receive_data = response_oes_msg

	def set_logon_values(self, logonObj):

		self.send_data['Account'] = logonObj.receive_data['Account']
		# self.send_data['TraderID'] = logonObj.receive_data['UserName']
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


def create_risk_user_symbol():
	message = RiskUserSymbol()
	return message
