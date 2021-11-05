# This file is for ClientLogon message

import struct
from base.message import Message
from constant.constant import LOGON_TYPE_LOGON


class ClientLogon(Message):
    """
    This class is for ClientLogon message
    """

    def __init__(self):
        super(ClientLogon, self).__init__()
        self.MessageName = "Client Logon"
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

        self.Data1 = "H"
        self.MessageLen = 143
        self.LogonType = LOGON_TYPE_LOGON
        self.TwoFA = 0
        self.UserName = ""
        self.PrimaryOrderEntryIP = ""
        self.SecondaryOrderEntryIP = ""
        self.PrimaryMarketDataIP = ""
        self.SecondaryMarketDataIP = ""
        self.LastSeqNum = 0
        self.LoginStatus = 0
        self.RiskMaster = ""

    def make_pack_struct(self):
        """
        build the binary struct for message
        """
        return struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")
