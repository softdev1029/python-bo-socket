"""
This file is for ClientLogon message
"""

import struct
from base.message import Message
from constant.logon_type import LOGIN, LOGOUT
import datetime as dt
from constant.types_management import logon
from constant.message_type import MSG_CLIENT_LOGON
import pyotp
import base64


class ClientLogon(Message):
    """
    This class is for ClientLogon message
    """

    def __init__(self):
        super(ClientLogon, self).__init__()
        self.MessageName = "Client Logon"
        self.module = logon
        self._names = (
            "Data1",
            "Data2",
            "MessageLen",
            "LogonType",
            "Account",
            "TwoFA",
            "UserName",
            "TradingSessionID",
            "PrimaryOrderEntryIP",
            "SecondaryOrderEntryIP",
            "PrimaryMarketDataIP",
            "SecondaryMarketDataIP",
            "SendingTime",
            "LastSeqNum",
            "Key",
            "LoginStatus",
            "RejectReason",
            "RiskMaster",
        )

        self.Data1 = MSG_CLIENT_LOGON
        self.MessageLen = 143
        self.LogonType = LOGIN
        self.TwoFA = 0
        self.UserName = ""
        self.PrimaryOrderEntryIP = ""
        self.SecondaryOrderEntryIP = ""
        self.PrimaryMarketDataIP = ""
        self.SecondaryMarketDataIP = ""
        self.LastSeqNum = 0
        self.LoginStatus = 0
        self.RiskMaster = ""

    def get_credential_info(self):
        self.MsgSeqID += 1
        return self.Account, self.UserName, self.Key, self.TradingSessionID, self.MsgSeqID

    def login(self, account, username, key, api_key):

        hotp = pyotp.HOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
        self.TwoFA = hotp.at(0)
        self.UserName = username
        self.Account = account
        self.Key = key
        self.SendingTime = int(dt.datetime.utcnow().timestamp() * 1e9)
        self.MsgSeqID = 0

    def make_pack_struct(self):
        """
        build the binary struct for message
        """
        return struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")

