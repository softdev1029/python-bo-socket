from auth.client_logon import ClientLogon
from base.socket_controller import SocketController
import time


class ResponserSocketController(SocketController):
    def __init__(self, sel, sock, addr, msgObj, recv_callback):
        super(ResponserSocketController, self).__init__(sel, sock, addr, msgObj, recv_callback)

        self._response_created = None

    def read(self):
        super(ResponserSocketController, self).read()

        self._set_selector_events_mask("w")

    def write(self):
        for i in range(1):
            # time.sleep(3)
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
            self.msgObj = message
            self.msgObj.encode()
            self._send_buffer = self.msgObj.binary_data
            self._write()

        self._set_selector_events_mask("r")
