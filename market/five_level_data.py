import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class FiveLevelData(Message):
    def __init__(self):
        super(FiveLevelData, self).__init__()
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
        # level 1
        Lvl1BuyPrice,
        Lvl1BuyVolume,
        Lvl1NumBuyOrders,
        Lvl1SellPrice,
        Lvl1SellVolume,
        Lvl1NumSellOrders,
        # level 2
        Lvl2BuyPrice,
        Lvl2BuyVolume,
        Lvl2NumBuyOrders,
        Lvl2SellPrice,
        Lvl2SellVolume,
        Lvl2NumSellOrders,
        # level 3
        Lvl3BuyPrice,
        Lvl3BuyVolume,
        Lvl3NumBuyOrders,
        Lvl3SellPrice,
        Lvl3SellVolume,
        Lvl3NumSellOrders,
        # level 4
        Lvl4BuyPrice,
        Lvl4BuyVolume,
        Lvl4NumBuyOrders,
        Lvl4SellPrice,
        Lvl4SellVolume,
        Lvl4NumSellOrders,
        # level 5
        Lvl5BuyPrice,
        Lvl5BuyVolume,
        Lvl5NumBuyOrders,
        Lvl5SellPrice,
        Lvl5SellVolume,
        Lvl5NumSellOrders,
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
            # level 1
            Lvl1BuyPrice,
            Lvl1BuyVolume,
            Lvl1NumBuyOrders,
            Lvl1SellPrice,
            Lvl1SellVolume,
            Lvl1NumSellOrders,
            # level 2
            Lvl2BuyPrice,
            Lvl2BuyVolume,
            Lvl2NumBuyOrders,
            Lvl2SellPrice,
            Lvl2SellVolume,
            Lvl2NumSellOrders,
            # level 3
            Lvl3BuyPrice,
            Lvl3BuyVolume,
            Lvl3NumBuyOrders,
            Lvl3SellPrice,
            Lvl3SellVolume,
            Lvl3NumSellOrders,
            # level 4
            Lvl4BuyPrice,
            Lvl4BuyVolume,
            Lvl4NumBuyOrders,
            Lvl4SellPrice,
            Lvl4SellVolume,
            Lvl4NumSellOrders,
            # level 5
            Lvl5BuyPrice,
            Lvl5BuyVolume,
            Lvl5NumBuyOrders,
            Lvl5SellPrice,
            Lvl5SellVolume,
            Lvl5NumSellOrders,
        )

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


def create_five_level_data():
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
        # level1
        60000.5,  # buyPrice
        60000.5,  # buyVolume
        5,  # numBuyOrders
        60000.5,  # sellPrice
        60000.5,  # sellVolume
        5,  # numSellOrders
        # level2
        60000.5,  # buyPrice
        60000.5,  # buyVolume
        5,  # numBuyOrders
        60000.5,  # sellPrice
        60000.5,  # sellVolume
        5,  # numSellOrders
        # level3
        60000.5,  # buyPrice
        60000.5,  # buyVolume
        5,  # numBuyOrders
        60000.5,  # sellPrice
        60000.5,  # sellVolume
        5,  # numSellOrders
        # level4
        60000.5,  # buyPrice
        60000.5,  # buyVolume
        5,  # numBuyOrders
        60000.5,  # sellPrice
        60000.5,  # sellVolume
        5,  # numSellOrders
        # level5
        60000.5,  # buyPrice
        60000.5,  # buyVolume
        5,  # numBuyOrders
        60000.5,  # sellPrice
        60000.5,  # sellVolume
        5,  # numSellOrders
    )
    return message
