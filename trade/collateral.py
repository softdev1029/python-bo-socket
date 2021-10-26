# This file is for Collateral message


import struct
from base.message import Message
from base.logger import log


class Collateral(Message):
    """
    This class is for Collateral message
    """

    def __init__(self):
        super(Collateral, self).__init__()
        self.msgType1 = None
        self.msgType2 = None
        self.length = None
        self.messageType = None
        self.padding = None
        self.userName = None
        self.account = None
        self.symbolEnum = None
        self.leverage = None
        self.longPosition = None
        self.shortPosition = None
        self.symbolDisabled = None
        self.accountEquity = None
        self.instrumentEquity = None
        self.executedLongCash = None
        self.executedLongPosition = None
        self.executedShortCash = None
        self.executedShortPosition = None
        self.btcEquity = None
        self.usdtEquity = None
        self.ethEquity = None
        self.usdEquity = None
        self.flyEquity = None
        self.openOrderRequestLimit = None
        self.TradingSessionID = None
        self.msgSeqNum = None
        self.binary_data = None

    def decode(self, data):
        try:
            s = struct.Struct("= H H 6s I H d d d d d 1s d d d d d d d d d d d I I I")
            unpacked_data = s.unpack(data[4:])
            log(unpacked_data)
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)
