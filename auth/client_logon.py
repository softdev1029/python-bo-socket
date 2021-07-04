import struct
from utils.helper import print_bytes_hex
from base.message import Message


class ClientLogon(Message):
    def __init__(self):
        super(ClientLogon, self).__init__()

        self.MessageType = 1000

        self.LogonType = None
        self.TwoFA = None
        self.UserName = None
        self.PrimaryOrderEntryIP = None
        self.SecondaryOrderEntryIP = None
        self.PrimaryMarketDataIP = None
        self.SecondaryMarketDataIP = None
        self.LastSeqNum = None
        self.LoginStatus = None
        self.RiskMaster = None

        self.data = ()
        self.binary_data = None

    def _set_data(self, *args):
        i = 0
        self.Data1 = args[i]
        i += 1
        self.Data2 = args[i]
        i += 1
        self.Data3 = args[i]
        i += 1
        self.LogonType = args[i]
        i += 1
        self.Account = args[i]
        i += 1
        self.TwoFA = args[i]
        i += 1
        self.UserName = args[i]
        i += 1
        self.TradingSessionID = args[i]
        i += 1
        self.PrimaryOrderEntryIP = args[i]
        i += 1
        self.SecondaryOrderEntryIP = args[i]
        i += 1
        self.PrimaryMarketDataIP = args[i]
        i += 1
        self.SecondaryMarketDataIP = args[i]
        i += 1
        self.SendingTime = args[i]
        i += 1
        self.LastSeqNum = args[i]
        i += 1
        self.Key = args[i]
        i += 1
        self.LoginStatus = args[i]
        i += 1
        self.RejectReason = args[i]
        i += 1
        self.RiskMaster = args[i]

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
            self._set_data(
                unpacked_data[0],
                unpacked_data[1],
                unpacked_data[2],
                unpacked_data[3],
                unpacked_data[4],
                unpacked_data[5],
                unpacked_data[6],
                unpacked_data[7],
                unpacked_data[8],
                unpacked_data[9],
                unpacked_data[10],
                unpacked_data[11],
                unpacked_data[12],
                unpacked_data[13],
                unpacked_data[14],
                unpacked_data[15],
                unpacked_data[16],
                unpacked_data[17],
            )
            is_valid = self.validate()
            print(
                "Decoded Client Logon message:",
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
