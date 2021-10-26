# This file is for ThirtyLevelData message


from market.base_level_data import BaseLevelData


class ThirtyLevelData(BaseLevelData):
    """
    This class is for ThirtyLevelData message
    """

    def __init__(self):
        super(ThirtyLevelData, self).__init__()
        self.data = ()
        self.binary_data = None
        self.level_count = 60  # Thirty Level Data message


def create_example_thirty_level_data():
    message = ThirtyLevelData()
    message.set_data(
        "U",  # data1
        "",  # data2
        1058,  # data3
        1,  # MessageType, BUY
        0,  # padding
        4,  # symbolEnum
        1,  # SymbolType SPOT,
        0,  # SendingTime
        1,  # MsgSeqNum
        1,  # StartLayer
        "BTCUSDT",  # Symbol
    )
    for i in range(60):
        message.set_extend_data(
            0,  # Price
            0,  # Volume
            0,  # Side
        )
    return message
