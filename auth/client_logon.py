import struct
from utils.helper import print_bytes_hex
from base.message import Message


class ClientLogon(Message):
    def __init__(self):
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.logonType = None
        self.account = None
        self.twoFA = None
        self.userName = None
        self.tradingSessionID = None
        self.primaryOrderEntryIP = None
        self.secondaryOrderEntryIP = None
        self.primaryMarketDataIP = None
        self.secondaryMarketDataIP = None
        self.sendingTime = None
        self.lastSeqNum = None
        self.key = None
        self.loginStatus = None
        self.rejectReason = None
        self.riskMaster = None

        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        logonType,
        account,
        twoFA,
        userName,
        tradingSessionID,
        primaryOrderEntryIP,
        secondaryOrderEntryIP,
        primaryMarketDataIP,
        secondaryMarketDataIP,
        sendingTime,
        lastSeqNum,
        key,
        loginStatus,
        rejectReason,
        riskMaster,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            logonType,
            account,
            twoFA.encode("utf-8"),
            userName.encode("utf-8"),
            tradingSessionID,
            primaryOrderEntryIP.encode("utf-8"),
            secondaryOrderEntryIP.encode("utf-8"),
            primaryMarketDataIP.encode("utf-8"),
            secondaryMarketDataIP.encode("utf-8"),
            sendingTime,
            lastSeqNum,
            key,
            loginStatus,
            rejectReason,
            riskMaster.encode("utf-8"),
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Client Logon message", self.binary_data, "")
            return True
        except Exception as e:
            print(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")
            unpacked_data = s.unpack(data)
            print(
                "Decoded Client Logon message",
                "\n\tdata1\t\t\t\t",
                unpacked_data[0],
                "\n\tdata2\t\t\t\t",
                unpacked_data[1],
                "\n\tdata3\t\t\t\t",
                unpacked_data[2],
                "\n\tlogonType\t\t\t",
                unpacked_data[3],
                "\n\taccount\t\t\t\t",
                unpacked_data[4],
                "\n\ttwoFA\t\t\t\t",
                unpacked_data[5],
                "\n\tuserName\t\t\t",
                unpacked_data[6],
                "\n\ttradingSessionID\t\t",
                unpacked_data[7],
                "\n\tprimaryOrderEntryIP\t\t",
                unpacked_data[8],
                "\n\tsecondaryOrderEntryIP\t\t",
                unpacked_data[9],
                "\n\tprimaryMarketDataIP\t\t",
                unpacked_data[10],
                "\n\tsecondaryMarketDataIP\t\t",
                unpacked_data[11],
                "\n\tsendingTime\t\t\t",
                unpacked_data[12],
                "\n\tlastSeqNum\t\t\t",
                unpacked_data[13],
                "\n\tkey\t\t\t\t",
                unpacked_data[14],
                "\n\tloginStatus\t\t\t",
                unpacked_data[15],
                "\n\trejectReason\t\t\t",
                unpacked_data[16],
                "\n\triskMaster\t\t\t",
                unpacked_data[17],
            )
            self.binary_data = data
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        self.decode(data)
        return True


def create_client_logon():
    message = ClientLogon()
    message.set_data(
        "H",  # data1
        "",  # data2
        143,  # data3
        1,  # LogonType
        253336,  # Account
        "1F6A",  # 2FA
        "BOU1",  # UserName
        1,  # TradingSessionID
        "1",  # PrimaryOESIP
        "1",  # SecondaryOESIP
        "1",  # PrimaryMDIP
        "1",  # SecondaryIP
        0,  # SendingTime
        1500201,  # MsgSeqNum
        432451,  # Key
        0,  # LoginStatus
        0,  # RejectReason
        "",  # RiskMaster
    )
    return message
