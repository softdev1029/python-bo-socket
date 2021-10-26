# This file is for TOBMsg message


import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class TOBMsg(Message):
    """
    This class is for TOBMsg message
    """

    def __init__(self):
        super(TOBMsg, self).__init__()
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
        symbolName,
        lastTradePrice,
        last24Vol,
        high,
        low,
        buyPrice,
        buyVolume,
        sellPrice,
        sellVolume,
        sendTime,
        seqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            padding,
            symbolEnum,
            symbolType,
            symbolName.encode("utf-8"),
            lastTradePrice,
            last24Vol,
            high,
            low,
            buyPrice,
            buyVolume,
            sellPrice,
            sellVolume,
            sendTime,
            seqNum,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H H H H 12s d d d d d d d d q I")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded TOB message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H H H 12s d d d d d d d d q I")
            unpacked_data = s.unpack(data)
            log("Decoded TOB message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_example_tob_msg():
    message = TOBMsg()
    message.set_data(
        "t",  # data1
        "",  # data2
        100,  # data3
        1,  # MessageType, BUY
        0,  # padding
        4,  # symbolEnum
        1,  # SymbolType SPOT,
        "BTCUSDT",  # symbolName
        60000.5,  # lastTradePrice
        60000.5,  # last24Vol
        60000.5,  # high
        60000.5,  # low
        60000.5,  # buyPrice
        60000.5,  # buyVolume
        60000.5,  # sellPrice
        60000.5,  # sellVolume
        18338102818181,  # sendTime
        52,  # seqNum
    )
    return message
