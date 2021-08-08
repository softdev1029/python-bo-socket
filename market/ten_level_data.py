import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class TenLevelData(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    def set_data(self, *data):
        self.data = [d if not isinstance(d, str) else d.encode("utf-8") for d in data]

    def set_extend_data(self, *data):
        self.data.extend(
            [d if not isinstance(d, str) else d.encode("utf-8") for d in data]
        )

    def encode(self):
        try:
            format = "= 1s 1s H H H H H q I H 12s"
            for i in range(20):
                format += " d d B"
            s = struct.Struct(format)
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Ten Level Data message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            format = "= 1s 1s H H H H H q I H 12s"
            for i in range(20):
                format += " d d B"
            s = struct.Struct(format)
            unpacked_data = s.unpack(data)
            log("Decoded Ten Level Data message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_ten_level_data():
    message = TenLevelData()
    message.set_data(
        "O",  # data1
        "",  # data2
        378,  # data3
        1,  # MessageType, BUY
        0,  # padding
        4,  # symbolEnum
        1,  # SymbolType SPOT,
        0,  # SendingTime
        1,  # MsgSeqNum
        1,  # StartLayer
        "BTCUSDT",  # Symbol
    )
    for i in range(20):
        message.set_extend_data(
            0,  # Price
            0,  # Volume
            0,  # Side
        )
    return message
