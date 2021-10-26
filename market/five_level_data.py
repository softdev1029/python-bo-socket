import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class FiveLevelData(Message):
    def __init__(self):
        super(FiveLevelData, self).__init__()
        self.data = ()
        self.binary_data = None
        self.level_count = 5  # Five Level Data message

    def encode(self):
        try:
            s = struct.Struct(
                "= 1s 1s H H H H H 12s d d d d d d H d d H d d H d d H d d H d d H d d H d d H d d H d d H"
            )
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded TOB message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct(
                "= 1s 1s H H H H H 12s d d d d d d H d d H d d H d d H d d H d d H d d H d d H d d H d d H"
            )
            unpacked_data = s.unpack(data)
            log("Decoded TOB message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_example_five_level_data():
    message = FiveLevelData()
    message.set_data(
        "m",  # data1
        "",  # data2
        164,  # data3
        1,  # MessageType, BUY
        0,  # padding
        4,  # symbolEnum
        1,  # SymbolType SPOT,
        "BTCUSDT",  # symbolName
        60000.5,  # lastTradePrice
        60000.5,  # last24Vol
        60000.5,  # high
        60000.5,  # low
    )
    for i in range(5):
        message.set_extend_data(
            60000.5,  # buyPrice
            60000.5,  # buyVolume
            5,  # numBuyOrders
            60000.5,  # sellPrice
            60000.5,  # sellVolume
            5,  # numSellOrders
        )

    return message
