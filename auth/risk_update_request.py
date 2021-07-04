import struct
from utils.helper import print_bytes_hex
from base.message import Message


class RiskUpdateRequest(Message):
    def __init__(self):
        super(RiskUpdateRequest, self).__init__()

    # 11 args
    def set_parsed_data(self, *args):
        i = 0
        self.Data1 = args[i]
        i += 1
        self.Data2 = args[i]
        i += 1
        self.Data3 = args[i]
        i += 1
        self.MessageType = args[i]
        i += 1
        self.ResponseType = args[i]
        i += 1
        self.Account = args[i]
        i += 1
        self.TradingSessionID = args[i]
        i += 1
        self.SymbolEnum = args[i]
        i += 1
        self.Key = args[i]
        i += 1
        self.MsgSeqNum = args[i]
        i += 1
        self.SendingTime = args[i]

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        responseType,
        account,
        tradingSessionID,
        symbolEnum,
        key,
        msgSeqNum,
        sendingTime,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            responseType,
            account,
            tradingSessionID,
            symbolEnum,
            key,
            msgSeqNum,
            sendingTime,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H H I I H I I Q")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Risk Update Request message", self.binary_data, "")
            return True
        except Exception as e:
            print(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H I I H I I Q")
            unpacked_data = s.unpack(data)
            self.set_parsed_data(
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
            )
            print(
                "Decoded Risk Update Request message:",
                "\n\tdata1\t\t\t\t",
                unpacked_data[0],
                "\n\tdata2\t\t\t\t",
                unpacked_data[1],
                "\n\tdata3\t\t\t\t",
                unpacked_data[2],
                "\n\tmessageType\t\t\t\t",
                unpacked_data[3],
                "\n\tresponseType\t\t\t\t",
                unpacked_data[4],
                "\n\taccount\t\t\t\t",
                unpacked_data[5],
                "\n\ttradingSessionID\t\t\t\t",
                unpacked_data[6],
                "\n\tsymbolEnum\t\t\t\t",
                unpacked_data[7],
                "\n\tkey\t\t\t\t",
                unpacked_data[8],
                "\n\tmsgSeqNum\t\t\t\t",
                unpacked_data[9],
                "\n\tsendingTime\t\t\t\t",
                unpacked_data[10],
            )
            self.binary_data = data
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        # self.decode(data)
        return True


def create_risk_update_request():
    message = RiskUpdateRequest()
    message.set_data(
        "w",  # data1
        "",  # data2
        34,  # data3
        0,  # MessageType
        2,  # ResponseType
        10070,  # account
        506,  # tradingSessionID
        1,  # SymbolEnum
        0,  # Key
        1005231,  # MsgSeqNum
        0,  # SendingTime
    )
    return message
