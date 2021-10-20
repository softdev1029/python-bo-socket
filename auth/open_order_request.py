import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class OpenOrderRequest(Message):
    def __init__(self):
        super(OpenOrderRequest, self).__init__()
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        Account,
        SymbolEnum,
        SymbolName,
        TradingSessionID,
        SendingTime,
        MsgSeqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            Account,
            SymbolEnum,
            SymbolName.encode("utf-8"),
            TradingSessionID,
            SendingTime,
            MsgSeqNum,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s h h i h 12s i q i")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Open Order Request message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s h h i h 12s i q i")
            unpacked_data = s.unpack(data)
            log("Decoded Open Order Request message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_open_order_request():
    message = OpenOrderRequest()
    message.set_data(
        "E",  # data1
        "",  # data2
        40,  # data3
        0,  # MessageType
        10070,  # account
        0,  # SymbolEnum
        "BTCUSD",  # SymbolName
        506,  # TradingSessionID
        0,  # SendingTime
        1500201,  # MsgSeqNum
    )
    return message
