# This file is for MDExecReport message


import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class MDExecReport(Message):
    """
    This class is for MDExecReport message
    """

    def __init__(self):
        super(MDExecReport, self).__init__()
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        padding,
        symbolEnum,
        symbolType,
        price,
        volume,
        sendTime,
        seqNum,
        side,
        symbolName,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            padding,
            symbolEnum,
            symbolType,
            price,
            volume,
            sendTime,
            seqNum,
            side,
            symbolName.encode("utf-8"),
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H H H H d d q I H 12s")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded MD Exec Report message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H H H d d q I H 12s")
            unpacked_data = s.unpack(data)
            log("Decoded MD Exec Report message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_example_md_exec_report():
    message = MDExecReport()
    message.set_data(
        "V",  # data1
        "",  # data2
        54,  # data3
        1,  # MessageType, ORDER_NEW
        0,  # padding
        4,  # symbolEnum
        1,  # SymbolType SPOT,
        60000.5,  # price
        1.3,  # volume
        18338102818181,  # sendTime
        52,  # seqNum
        1,  # side, BUY
        "BTCUSDT",  # symbolName
    )
    return message
