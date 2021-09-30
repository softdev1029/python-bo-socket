import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class InstrumentRequest(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        rejectReason,
        account,
        requestType,
        key,
        symbolName,
        symbolType,
        symbolEnum,
        tradingSessionID,
        sendingTime,
        msgSeqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            rejectReason,
            account,
            requestType,
            key,
            symbolName.encode("utf-8"),
            symbolType,
            symbolEnum,
            tradingSessionID,
            sendingTime,
            msgSeqNum,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H I I H I 24s H H I Q I")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Instrument Request message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H I I H I 24s H H I Q I")
            unpacked_data = s.unpack(data)
            log("Decoded Instrument Request message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_instrument_request(aes_or_oes_key):
    message = InstrumentRequest()
    message.set_data(
        "Y",  # data1
        "",  # data2
        64,  # data3
        0,  # MessageType
        0,  # RejectReason
        100700,  # Account
        2,  # RequestType
        aes_or_oes_key,  # Key
        "",  # SymbolName
        0,  # SymbolType
        0,  # SymbolEnum
        506,  # TradingSessionID
        0,  # SendingTime
        1500201,  # MsgSeqNum
    )
    return message
