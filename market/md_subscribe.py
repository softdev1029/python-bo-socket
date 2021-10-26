# This file is for MDSubscribe message


import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class MDSubscribe(Message):
    """
    This class is for MDSubscribe message
    """

    def __init__(self):
        super(MDSubscribe, self).__init__()
        self.data = ()
        self.binary_data = None

    def encode(self):
        try:
            format = "= 1s 1s H H H I I I q I"
            for i in range(5):
                format += " H 16s H H 1s"
            s = struct.Struct(format)
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded MD Subscribe message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            format = "= 1s 1s H H H I I I q I"
            for i in range(5):
                format += " H 16s H H 1s"
            s = struct.Struct(format)
            unpacked_data = s.unpack(data)
            log("Decoded MD Subscribe message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_example_md_subscribe():
    message = MDSubscribe()
    message.set_data(
        "s",  # data1
        "",  # data2
        147,  # 32,  # data3
        1,  # MessageType, TOB
        0,  # padding
        100700,  # account
        468321,  # key
        200,  # tradingSessionID
        184232029271,  # sendTime
        52488131,  # seqNum
    )
    for i in range(5):
        message.set_extend_data(
            0,  # SymbolEnum
            "BTCUSDT",  # Symbol
            1,  # SymbolType
            1,  # Layers
            "S",  # Subscribe
        )
    return message
