import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class ClientLogon(Message):
    def __init__(self):
        super(ClientLogon, self).__init__()
        self.MessageName = "Client Logon"
        self._names = (
            "Data1",
            "Data2",
            "Data3",
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

    def make_pack_struct(self):
        return struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")


def create_client_logon(aes_or_oes_key):
    message = ClientLogon()
    message.set_data(
        "H",  # data1
        "",  # data2
        143,  # data3
        1,  # LogonType
        100700,  # Account
        "1F6A",  # 2FA
        "BOU7",  # UserName
        506,  # TradingSessionID
        "1",  # PrimaryOESIP
        "1",  # SecondaryOESIP
        "1",  # PrimaryMDIP
        "1",  # SecondaryIP
        0,  # SendingTime
        1500201,  # MsgSeqNum
        aes_or_oes_key,  # Key
        0,  # LoginStatus
        0,  # RejectReason
        "",  # RiskMaster
    )
    return message
