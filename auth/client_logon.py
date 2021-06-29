import struct


class ClientLogon:
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
        logonType,
        account,
        twoFA,
        userName,
        tradingSessionID,
        primaryOrderEntryIP,
        secondaryOrderEntryIP,
        primaryMarketDataIP,
        secondaryMarketDataIP,
        sendingTime,
        lastSeqNum,
        key,
        loginStatus,
        rejectReason,
        riskMaster,
    ):
        self.data = (
            data1,
            data2,
            data3,
            logonType,
            account,
            twoFA,
            userName,
            tradingSessionID,
            primaryOrderEntryIP,
            secondaryOrderEntryIP,
            primaryMarketDataIP,
            secondaryMarketDataIP,
            sendingTime,
            lastSeqNum,
            key,
            loginStatus,
            rejectReason,
            riskMaster,
        )

    def encode_binary_string(self):
        try:
            s = struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")
            self.binary_data = s.pack(*(self.data))
            print("Encoded Client Logon message", self.binary_data)
            return True
        except Exception as e:
            print(e)
            return False

    def decode_binary_string(self, data):
        try:
            s = struct.Struct("= 1s 1s H H I 6s 6s I 24s 24s 24s 24s Q I I H H 1s")
            unpacked_data = s.unpack(data)
            print("Decoded Client Logon message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        return self.decode_binary_string(data)
