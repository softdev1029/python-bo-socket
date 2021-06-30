import struct
from utils.helper import print_bytes_hex
from base.message import Message


class InstrumentResponse(Message):
    def __init__(self):
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.logonType = None
        self.account = None
        self.twoFA = None
        self.userName = None
        self.tradingSessionID = None
        self.primaryOrderEntryIP = None
        self.secondaryOrderEntryIP = None
        self.primaryMarketDataIP = None
        self.secondaryMarketDataIP = None
        self.sendingTime = None
        self.lastSeqNum = None
        self.key = None
        self.loginStatus = None
        self.rejectReason = None
        self.riskMaster = None

        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        padding,
        responseType,
        symbolEnum,
        symbolName,
        symbolType,
        priceIncrement,
        minSize,
        maxSize,
        sendingTime,
        msgSeqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            padding,
            responseType,
            symbolEnum,
            symbolName.encode("utf-8"),
            symbolType,
            priceIncrement,
            minSize,
            maxSize,
            sendingTime,
            msgSeqNum,
        )

    def encode_binary_string(self):
        try:
            s = struct.Struct("= 1s 1s H H H H H 24s H e e e Q I")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Instrument Response message", self.binary_data, "")
            return True
        except Exception as e:
            print(e)
            return False

    def decode_binary_string(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H H H 24s H e e e Q I")
            unpacked_data = s.unpack(data)
            print("Decoded Instrument Response message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        self.encode_binary_string()
        return True
