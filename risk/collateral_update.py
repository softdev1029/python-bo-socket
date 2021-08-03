"""
module for calling server for collateral values, means values of equity on different currencies
"""
from base.message import Message
import datetime as dt
import numpy as np


send_msg = {
	"msg1": "f",
	"UpdateType": 2
}

# example of server response
response_oes_msg = {
	"msg1": "h",
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


class CollateralUpdate(Message):

	def __init__(self):
		"""
		class which looks for our values of equities in different currencies
		"""
		super(CollateralUpdate, self).__init__()

		self.send_data = send_msg
		self.receive_data = response_oes_msg

	def set_logon_values(self, logonObj):
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


def create_collateral_update():
	"""
	creating message with collateral request
	:return:
	"""
	message = CollateralUpdate()

	return message
