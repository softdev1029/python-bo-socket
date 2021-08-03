"""
client logon module
"""
from base.message import Message
import json
import datetime as dt

send_msg = {
	"msg1": "H",
	"LogonType": 1,
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
	"LogonType": 1,
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


class ClientLogon(Message):
	def __init__(self, account: int, username: str, key: int, tradingsessionID: int) -> None:
		super(ClientLogon, self).__init__()

		self.send_data = send_msg
		self.send_data['Account'] = account
		self.send_data['UserName'] = username
		self.send_data['SendingTime'] = int(dt.datetime.utcnow().timestamp() * 1e9)
		self.send_data['TradingSessionID'] = tradingsessionID
		self.send_data['Key'] = key
		self.send_data['MsgSeqID'] = 0
		self.send_data['RiskMaster'] = 'N'
		self.receive_data = response_oes_msg

def create_client_logon():

	# message = ClientLogon(account=90001, username="MTX01", key=123456, tradingsessionID=901)
	message = ClientLogon(account=100700, username="BOU7", key=123456, tradingsessionID=506)
	return message
