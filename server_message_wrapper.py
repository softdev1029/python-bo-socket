from auth.client_logon import ClientLogon
from base.message_wrapper import MessageWrapper


class ServerMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ServerMessageWrapper, self).__init__(sel, sock, addr, msgObj)

        self._response_created = None

    def read(self):
        super(ServerMessageWrapper, self).read()

        message = ClientLogon()
        message.set_data(
            "H",  # data1
            "",  # data2
            143,  # data3
            1,  # LogonType
            100700,  # Account
            "1F6A",  # 2FA
            "BOU7",  # UserName
            506,  # TradingSessionID
            "1",  # PrimaryOESIP
            "1",  # SecondaryOESIP
            "1",  # PrimaryMDIP
            "1",  # SecondaryIP
            0,  # SendingTime
            1500201,  # MsgSeqNum
            432451,  # Key
            0,  # LoginStatus
            0,  # RejectReason
            "",  # RiskMaster
        )
        self.msgObj.encode()
        self.msgObj = message
        self._set_selector_events_mask("w")

    def write(self):
        self._write()
        self._set_selector_events_mask("r")
