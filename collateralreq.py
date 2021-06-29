import struct

class CollateralReq:
    def __init__(self):
        self.data = ()
        self.binary_data = None
    
    def set_data(
        self,
        msgType1,
        msgType2,
        length,
        messageType,
        updateType,
        account,
        tradingSessionID,
        symbolEnum,
        key,
        msgSeqNum,
        sendingTime
    ):
        self.data = (
            msgType1.encode('utf-8'),
            msgType2.encode('utf-8'),
            length,
            messageType,
            updateType,
            account,
            tradingSessionID,
            symbolEnum,
            key,
            msgSeqNum,
            sendingTime
        )

    def encode_binary_string(self):
        try:
            s = struct.Struct('= 1s 1s H H H I I H I I Q')
            self.binary_data = s.pack(*(self.data))
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        self.encode_binary_string()
        return True