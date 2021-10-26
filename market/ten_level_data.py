# This file is for TenLevelData message


from market.base_level_data import BaseLevelData


class TenLevelData(BaseLevelData):
    """
    This class is for TenLevelData message
    """

    def __init__(self):
        super(TenLevelData, self).__init__()
        self.data = ()
        self.binary_data = None
        self.level_count = 20  # Ten Level Data message


def create_example_ten_level_data():
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
