"""
It is for defining fundamental message
"""
import struct
from constant import reject_code, message_type, order_type, attribute_type, order_message_type
from base.logger import log
from utils.helper import print_bytes_hex
from constant.types_management import reject, message, order, symbol, side, order_message, MAX_LAYERS
from constant.message_type import MSG_INSTRUMENT_REQUEST, MSG_INSTRUMENT_RESPONSE
import datetime as dt


class Message:
    """
    It is the basic class for all messages
    """

    def __init__(self):
        self.MessageName = ""
        self.data = None
        self.binary_data = None
        self._names = ()

        self.Data1 = ""
        self.Data2 = ""
        self.MessageLen = 0
        self.MessageType = 0
        self.Padding = 0
        self.Account = 0
        self.OrderID = 0
        self.SymbolEnum = 0
        self.OrderType = 0
        self.SymbolType = 0
        self.BOPrice = 0
        self.BOSide = 0
        self.BOOrderQty = 0
        self.TIF = 0
        self.StopLimitPrice = 0
        self.BOSymbol = ""
        self.OrigOrderID = 0
        self.BOCancelShares = 0
        self.ExecID = 0
        self.ExecShares = 0
        self.RemainingQuantity = 0
        self.ExecFee = 0
        self.ExpirationDate = ""
        self.TraderID = ""
        self.RejectReason = 0
        self.SendingTime = 0
        self.TradingSessionID = 0
        self.Key = 0
        self.DisplaySize = 0
        self.RefreshSize = 0
        self.Layers = 0
        self.SizeIncrement = 0
        self.PriceIncrement = 0
        self.PriceOffset = 0
        self.BOOrigPrice = 0
        self.ExecPrice = 0
        self.MsgSeqNum = 0
        self.TakeProfitPrice = 0
        self.TriggerType = 0
        self.SecondLegPrice = 0
        self.RouteEnum = 0
        self.ModifyType = 0
        self.Attributes = ""

        pass

    def set_data(self, *data):
        if len(data) == len(self._names):
            self.data = [
                d if not isinstance(d, str) else d.encode("utf-8") for d in data
            ]
            for i, d in enumerate(self.data):
                self.__setattr__(self._names[i], d)
        else:
            raise Exception("Message has not valid length of fields")

    def set_extend_data(self, *data):
        self.data.extend(
            [d if not isinstance(d, str) else d.encode("utf-8") for d in data]
        )

    def make_pack_struct(self):
        return struct.Struct()

    def encode(self):
        try:
            s = self.make_pack_struct()
            if self.data is None:
                self.data = []
                self.data.extend(
                    [
                        self.__getattribute__(name)
                        if not isinstance(self.__getattribute__(name), str)
                        else self.__getattribute__(name).encode("utf-8")
                        for name in self._names
                    ]
                )
            # print("To check each Message Field type...")
            # for n in self.data:
            #     print(n)
            self.binary_data = s.pack(*self.data)
            print_bytes_hex(
                "Encoded {} message".format(self.MessageName), self.binary_data, ""
            )
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)

    def decode(self, data):
        try:
            s = self.make_pack_struct()
            unpacked_data = s.unpack(data)
            self.set_data_from_decoded(*unpacked_data)
            self.print_message()
            is_valid = True
            if self.Data1 in [MSG_INSTRUMENT_REQUEST, MSG_INSTRUMENT_RESPONSE]:
                is_valid = self.validate_order()
            log("Valid:", is_valid)
            if is_valid is False:
                self.print_reject_reason()
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def set_data_from_decoded(self, *data):
        for i, d in enumerate(data):
            self.__setattr__(
                self._names[i], d if not isinstance(d, bytes) else d.decode("utf-8")
            )

    def print_message(self):
        for d in self._names:
            log("\t", d, ": ", self.__getattribute__(d))

    def print_reject_reason(self):
        log("Reject Code: ", self.RejectReason)
        msg = f"Reject Reason: {reject.get_description(self.RejectReason)}"
        log(msg)

    def _validate_msg_types(self, msg_type: int) -> bool:
        """
        validation based on message type
        :param msg_type: int
        :return: bool
        """
        msg = {order_type.ICE: self._validate_ICE(),
               order_type.OCO: self._validate_OCO(),
               order_type.OCO_ICE: self._validate_OCO() and self._validate_ICE()
              }

        return msg.setdefault(msg_type, True)

    def _validate_ord_types(self, ord_type: int) -> bool:
        """
        validation based on order type
        :param ord_type: int
        :return: bool
        """
        if ord_type in [
                order_message_type.CANCEL_REPLACE,
                order_message_type.ORDER_CANCEL,
                order_message_type.MARGIN_CANCEL_REPLACE,
                order_message_type.MARGIN_CANCEL
                ]:
            return self._validate_cancel_order()

        return True

    def validate_order(self) -> bool:
        """
        main validation of all parameters
        :return:
        """
        if not order_message.is_valid(self.MessageType):
            self.RejectReason = reject_code.MSG_TYPE_INVALID
            return False

        if not order.is_valid(self.OrderType):
            self.RejectReason = reject_code.ORD_TYPE_INVALID
            return False

        if not symbol.is_valid(self.SymbolEnum):
            self.RejectReason = reject_code.SYMBOL_ENUM_INVALID
            return False

        #TODO why Trading SessionID can be less 0 if it os set on server side
        if self.TradingSessionID < 0:
            self.RejectReason = reject_code.TRADING_SESSION_INVALID
            return False

        if not side.is_valid(self.BOSide):
            self.RejectReason = reject_code.ORDER_SIDE_INVALID
            return False

        #TODO why we check so obvious situation
        if self.Account <= 0:
            self.RejectReason = reject_code.ACCOUNT_INVALID
            return False

        if self.OrderID <= 0:
            self.RejectReason = reject_code.ORDERID_INVALID
            return False

        #we are checking if sending time is in range of 1 day before and 1 day after current time
        day_before = int((dt.datetime.utcnow() - dt.timedelta(days=1)).timestamp() * 1e9)
        day_after = int((dt.datetime.utcnow() + dt.timedelta(days=1)).timestamp() * 1e9)

        if not day_before < self.SendingTime < day_after:
            self.RejectReason = reject_code.SENDING_TIME_INVALID
            return False

        return self._validate_msg_types(self.MessageType) and self._validate_ord_types(self.OrderType)

    def _validate_ICE(self) -> bool:
        """
        validate ICE order
        :return:
        """
        if self.Layers > MAX_LAYERS:
            self.RejectReason = reject_code.EXCEEDED_MAX_LAYERS
            return False

        if self.SizeIncrement <= 0:
            self.RejectReason = reject_code.SIZE_INCREMENT_INVALID
            return False

        if self.PriceOffset < 0:
            self.RejectReason = reject_code.PRICE_OFFSET_INVALID
            return False

        if self.PriceIncrement < 0:
            self.RejectReason = reject_code.PRICE_INCREMENT_INVALID
            return False

        return True

    def _validate_OCO(self) -> bool:
        """
        validate OCO order
        :return:
        """
        if self.StopLimitPrice <= 0:
            self.RejectReason = reject_code.STOP_PRICE_INVALID
            return False

        return True

    def _validate_cancel_order(self) -> bool:
        """
        validate cancel and calncel_replace order
        :return:
        """
        if self.OrigOrderID <= 0:
            self.RejectReason = reject_code.ORIG_ORDER_ID_INVALID
            return False

        return True


def create_example_base_message():
    message = Message()
    return message
