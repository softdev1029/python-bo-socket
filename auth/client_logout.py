"""
client logon module
"""
from base.message import Message
import numpy as np
import datetime as dt

send_msg = {
	"msg1": "H",
	"LogonType": 2,
	"Account": None,
	"UserName": None,
	"TradingSessionID": None,
	"SendingTime": None,
	"MsgSeqID": None,
	"Key": None,
	"RiskMaster": 'N'
}


response_oes_msg = {
	"msg1": "H",
	"LogonType": 2,
	"Account": None,
	"UserName": None,
	"TradingSessionID": None,
	"SendingTime": None,
	"MsgSeqID": None,
	"Key": None,
	"LoginStatus": None,
	"RejectReason": None,
	"RiskMaster": None
}


class ClientLogout(Message):
	def __init__(self) -> None:
		super(ClientLogout, self).__init__()

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


def create_client_logout():

	message = ClientLogout()
	return message
