import struct
import binascii
from base.message import Message


class Collateral(Message):
    def __init__(self):
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

    def decode_binary_string(self, data):
        try:
            s = struct.Struct("= H H 6s I H d d d d d 1s d d d d d d d d d d d I I I")
            unpacked_data = s.unpack(data[4:])
            print(unpacked_data)
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        try:
            s = struct.Struct("= 1s 1s H")
            unpacked_data = s.unpack(data[:4])
            if unpacked_data[-1] == 161:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def parse_message(self, data):
        return self.decode_binary_string(data)
