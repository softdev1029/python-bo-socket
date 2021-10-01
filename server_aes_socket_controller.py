from auth.client_logon import ClientLogon
from transaction.transaction import Transaction
from base.socket_controller import SocketController
import time

process_state = "send_logon_reply"


class ResponserSocketController(SocketController):
    def __init__(self, sel, sock, addr, msgObj, recv_callback):
        super(ResponserSocketController, self).__init__(
            sel, sock, addr, msgObj, recv_callback
        )

        self._response_created = None

    def read(self):
        super(ResponserSocketController, self).read()

        self._set_selector_events_mask("w")

    def write(self):
        global process_state
        print("process_state=", process_state)
        for i in range(1):
            # time.sleep(3)
            if process_state == "send_logon_reply":
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
                    "127.0.0.1:4445",  # PrimaryOESIP
                    "1",  # SecondaryOESIP
                    "1",  # PrimaryMDIP
                    "1",  # SecondaryIP
                    0,  # SendingTime
                    1500201,  # MsgSeqNum
                    432451,  # Key
                    1,  # LoginStatus, success
                    0,  # RejectReason
                    # 2,  # LoginStatus, fail
                    # 4,  # RejectReason, INVALID_KEY
                    "",  # RiskMaster
                )
            self.msgObj = message
            self.msgObj.encode()
            self._send_buffer = self.msgObj.binary_data
            self._write()

        self._set_selector_events_mask("r")
