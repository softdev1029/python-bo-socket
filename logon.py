import struct

class Logon:
    def __init__(self):
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.padding = None
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
        self.binary_data = None

    def decode_binary_string(self, data):
        try:
            s = struct.Struct('= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s')
            unpacked_data = s.unpack(data)
            print(unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            print(e)
            return False
    
    def parse_header(self, data):
        return True


    def parse_message(self, data):
        return self.decode_binary_string(data)
