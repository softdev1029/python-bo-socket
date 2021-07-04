import struct
from utils.helper import print_bytes_hex
from base.message import Message


class RiskUpdateRequest(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

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
            print("Decoded Risk Update Request message", unpacked_data)
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
