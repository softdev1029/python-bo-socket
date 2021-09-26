from auth.client_logon import ClientLogon
from transaction.new_limit_order import NewLimitOrder
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
                process_state = "send_order_reply"
            elif process_state == "send_order_reply":
                message = NewLimitOrder()
                message.set_data(
                    "T",  # data1,
                    "",  # data2,
                    238,  # data3,
                    14,  # messageType ORDER_ACK
                    0,  # padding,
                    100700,  # account,
                    46832151,  # orderID,
                    1,  # symbolEnum,
                    1,  # OrderType LMT
                    1,  # SymbolType SPOT
                    50100.5,  # BOPrice,
                    3,  # BOSide BUY
                    2.0,  # BOOrderQty,
                    2,  # TIF -> GTC
                    0,  # StopLimitPrice,
                    "BTCUSD",  # BOSymbol,
                    0,  # OrigOrderID,
                    0,  # BOCancelShares,
                    0,  # ExecID,
                    0,  # ExecShares,
                    0,  # RemainingQuantity,
                    0,  # ExecFee,
                    "",  # ExpirationDate,
                    "",  # TraderID,
                    0,  # RejectReason,
                    1000,  # SendingTime,
                    506,  # TradingSessionID,
                    42341,  # Key,
                    0,  # DisplaySize,
                    0,  # RefreshSize,
                    0,  # Layers,
                    0,  # SizeIncrement,
                    0,  # PriceIncrement,
                    0,  # PriceOffset,
                    0,  # BOOrigPrice,
                    0,  # ExecPrice,
                    79488880,  # MsgSeqNum,
                    0,  # TakeProfitPrice,
                    0,  # TriggerType,
                    1111,  # SecondLegPrice,
                    1,  # RouteEnum,
                    1,  # ModifyType,
                    "",  # Attributes,
                )
            self.msgObj = message
            self.msgObj.encode()
            self._send_buffer = self.msgObj.binary_data
            self._write()

        self._set_selector_events_mask("r")
