from market.base_level_data import BaseLevelData


class TwentyLevelData(BaseLevelData):
    def __init__(self):
        super(TwentyLevelData, self).__init__()
        self.data = ()
        self.binary_data = None
        self.level_count = 40  # Twenty Level Data message


def create_twenty_level_data():
    message = TwentyLevelData()
    message.set_data(
        "S",  # data1
        "",  # data2
        718,  # data3
        1,  # MessageType, BUY
        0,  # padding
        4,  # symbolEnum
        1,  # SymbolType SPOT,
        0,  # SendingTime
        1,  # MsgSeqNum
        1,  # StartLayer
        "BTCUSDT",  # Symbol
    )
    for i in range(40):
        message.set_extend_data(
            0,  # Price
            0,  # Volume
            0,  # Side
        )
    return message
