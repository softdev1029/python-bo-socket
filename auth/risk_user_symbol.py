# This file is for RiskUserSymbol message


import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class RiskUserSymbol(Message):
    """
    This class is for RiskUserSymbol message
    """

    def __init__(self):
        super(RiskUserSymbol, self).__init__()
        self.data = ()
        self.binary_data = None
        self.decoded_data = {}
        self._names = (
            "data1",
            "data2",
            "data3",
            "messageType",
            "padding",
            "userName",
            "account",
            "symbolEnum",
            "leverage",
            "longPosition",
            "shortPosition",
            "longCash",
            "shortCash",
            "symbolDisabled",
            "accountEquity",
            "instrumentEquity",
            "executedLongCash",
            "executedLongPosition",
            "executedShortCash",
            "executedShortPosition",
            "BTCEquity",
            "USDTEquity",
            "ETHEquity",
            "USDEquity",
            "FLYEquity",
            "openOrderRequestLimit",
            "tradingSessionID",
            "msgSeqNum",
        )

    def set_data(self, *data):
        if len(data) == len(self._names):
            self.data = [
                d if not isinstance(d, str) else d.encode("utf-8") for d in data
            ]
        else:
            raise Exception("Message has not valid length")

    def encode(self):
        try:
            s = struct.Struct(
                "= 1s 1s H H H 6s I H d d d d d B d d d d d d d d d d d I I I"
            )
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Risk User Symbol message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct(
                "= 1s 1s H H H 6s I H d d d d d B d d d d d d d d d d d I I I"
            )
            unpacked_data = s.unpack(data)
            self.set_data_from_decoded(*unpacked_data)
            log("Decoded Risk User Symbol message", self.decoded_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False


def create_example_risk_user_symbol():
    message = RiskUserSymbol()
    message.set_data(
        "N",  # data1
        "",  # data2
        34,  # data3
        0,  # MessageType
        0,  # Padding
        "NAM1",  # UserName
        100700,  # Account
        1,  # SymbolEnum
        0,  # Leverage
        3.0,  # LongPosition
        5.0,  # ShortPosition
        51000,  # LongCash
        52000,  # ShortCash
        0,  # SymbolDisabled
        0,  # AccountEquity
        0,  # InstrumentEquity
        150000,  # ExecutedLongCash
        3,  # ExecutedLongPosition
        102000,  # ExecutedShortCash
        2,  # ExecutedShortPosition
        25,  # BTCEquity
        500000,  # USDTEquty
        1000,  # ETHEquity
        1000000,  # USDEquity
        400000,  # FLYEquity
        1000,  # OpenOderRequestLimit
        506,  # TradingSessionID
        42431,  # MsgSeqNum
    )
    return message
