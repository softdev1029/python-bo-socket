from auth.client_logon import ClientLogon
from base.message_controller import MessageController
import time


class ServerMessageController(MessageController):
    def __init__(self, sel, sock, addr, msgObj):
        super(ServerMessageController, self).__init__(sel, sock, addr, msgObj)

        self._response_created = None

    def read(self):
        super(ServerMessageController, self).read()

        self._set_selector_events_mask("w")

    def write(self):
        for i in range(2):
            # time.sleep(3)
            message = ClientLogon()
            message.set_data(
                "H",  # data1
                "",  # data2
                256,  # data3
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
            self.msgObj = message
            self.msgObj.encode()
            self._send_buffer = self.msgObj.binary_data
            self._write()

        self._set_selector_events_mask("r")
