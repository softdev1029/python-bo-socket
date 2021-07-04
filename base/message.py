from constant import constant, reject_code, message_type, order_type, attribute


class Message:
    def __init__(self):
        self.Data1 = None
        self.Data2 = None
        self.Data3 = None
        self.MessageType = None
        self.Padding = None
        self.Account = None
        self.OrderID = None
        self.SymbolEnum = None
        self.OrderType = None
        self.SymbolType = None
        self.BOPrice = None
        self.BOSide = None
        self.BOOrderQty = None
        self.TIF = None
        self.StopLimitPrice = None
        self.BOSymbol = None
        self.OrigOrderID = None
        self.BOCancelShares = None
        self.ExecID = None
        self.ExecShares = None
        self.RemainingQuantity = None
        self.ExecFee = None
        self.ExpirationDate = None
        self.TraderID = None
        self.RejectReason = None
        self.SendingTime = None
        self.TradingSessionID = None
        self.Key = None
        self.DisplaySize = None
        self.RefreshSize = None
        self.Layers = None
        self.SizeIncrement = None
        self.PriceIncrement = None
        self.PriceOffset = None
        self.BOOrigPrice = None
        self.ExecPrice = None
        self.MsgSeqNum = None
        self.TakeProfitPrice = None
        self.TriggerType = None
        self.Attributes = None

        pass

    def set_data(self, *args):
        pass

    def encode(self):
        return False

    def decode(self, data):
        return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        return True

    def validate(self):
        if (
            self.MessageType < constant.MSGTYPE_MIN_VALUE
            or self.MessageType > constant.ORDTYPE_MAX_VALUE
        ):
            self.RejectReason = reject_code.MSG_TYPE_INVALID
            return False

        if (
            self.OrderType < constant.ORDTYPE_MIN_VALUE
            or self.OrderType > constant.ORDTYPE_MAX_VALUE
        ):
            self.RejectReason = reject_code.ORD_TYPE_INVALID
            return False

        if self.MessageType is message_type.ORDER_NEW:
            if self.OrderType in [
                order_type.LMT,
                order_type.HIDDEN,
                order_type.PEG,
                order_type.PEG_HIDDEN,
                order_type.OCO,
                order_type.ICE,
            ]:
                ds = self.Attributes[attribute.DISPLAYSIZE_ATTRIBUTE]
                if ds == "Y":
                    if self.DisplaySize <= 0:
                        self.RejectReason = reject_code.DISPLAY_SIZE_INVALID

                if self.RejectReason <= 0:
                    self.RejectReason = reject_code.REFRESH_SIZE_INVALID

                se = self.SymbolEnum
                if se < constant.SE_MIN_VALUE or se > constant.SE_MAX_VALUE:
                    self.RejectReason = reject_code.SYMBOL_ENUM_INVALID
                    return False

                if self.TradingSessionID < 0:
                    self.RejectReason = reject_code.TRADING_SESSION_INVALID
                    return False

                if self.BOPrice < constant.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.PRICE_INVALID
                    return False

                if self.BOOrderQty < constant.ORDER_MIN_SIZE:
                    self.RejectReason = reject_code.SIZE_INVALID
                    return False

                side = self.BOSide
                if side < 1 or side > 3:
                    self.RejectReason = reject_code.ORDER_SIDE_INVALID
                    return False

                if self.Account <= 0:
                    self.RejectReason = reject_code.ACCOUNT_INVALID
                    return False

                if self.OrderID <= 0:
                    self.RejectReason = reject_code.ORDERID_INVALID
                    return False

                if self.SendingTime <= 0:
                    self.RejectReason = reject_code.SENDING_TIME_INVALID
                    return False

            if self.OrderType is order_type.ICE:
                if self.Layers > constant.MAX_LAYERS:
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

            if self.OrderType is order_type.OCO:
                if self.StopLimitPrice <= 0:
                    self.RejectReason = reject_code.STOP_PRICE_INVALID
                    return False

        elif self.MessageType is message_type.ORDER_CANCEL:
            if self.OrderType in [
                order_type.LMT,
                order_type.HIDDEN,
                order_type.PEG,
                order_type.PEG_HIDDEN,
                order_type.OCO,
                order_type.ICE,
            ]:
                se = self.SymbolEnum
                if se < constant.SE_MIN_VALUE or se > constant.SE_MAX_VALUE:
                    self.RejectReason = reject_code.SYMBOL_ENUM_INVALID
                    return False

                if self.BOPrice < order_type.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.PRICE_INVALID
                    return False

                if self.BOOrigPrice < order_type.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.ORIG_PRICE_INVALID
                    return False

                side = self.BOSide
                if side < 1 or side > 3:
                    self.RejectReason = reject_code.ORDER_SIDE_INVALID
                    return False

                if self.Account <= 0:
                    self.RejectReason = reject_code.ACCOUNT_INVALID
                    return False

                if self.OrderID <= 0:
                    self.RejectReason = reject_code.ORDERID_INVALID
                    return False

                if self.OrigOrderID <= 0:
                    self.RejectReason = reject_code.ORIG_ORDER_ID_INVALID
                    return False

                if self.SendingTime <= 0:
                    self.RejectReason = reject_code.SENDING_TIME_INVALID
                    return False

        elif self.MessageType is message_type.CANCEL_REPLACE:
            if self.OrderType in [
                order_type.LMT,
                order_type.HIDDEN,
                order_type.PEG,
                order_type.PEG_HIDDEN,
                order_type.OCO,
                order_type.ICE,
            ]:
                attributes = self.Attributes
                ds = attributes[attribute.DISPLAYSIZE_ATTRIBUTE]
                if ds == "Y":
                    if self.DisplaySize <= 0:
                        self.RejectReason = reject_code.DISPLAY_SIZE_INVALID

                    if self.RefreshSize <= 0:
                        self.RejectReason = reject_code.REFRESH_SIZE_INVALID

                se = self.SymbolEnum
                if se < constant.SE_MIN_VALUE or se > constant.SE_MAX_VALUE:
                    self.RejectReason = reject_code.SYMBOL_ENUM_INVALID
                    return False

                if self.BOPrice < constant.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.PRICE_INVALID
                    return False

                if self.OrigOrderID < constant.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.ORIG_PRICE_INVALID
                    return False

                side = self.BOSide
                if side < 1 or side > 3:
                    self.RejectReason = reject_code.ORDER_SIDE_INVALID
                    return False

                if self.Account <= 0:
                    self.RejectReason = reject_code.ACCOUNT_INVALID
                    return False

                if self.OrderID <= 0:
                    self.RejectReason = reject_code.ORDERID_INVALID
                    return False

                if self.OrigOrderID <= 0:
                    self.RejectReason = reject_code.ORIG_ORDER_ID_INVALID
                    return False

                if self.SendingTime <= 0:
                    self.RejectReason = reject_code.SENDING_TIME_INVALID
                    return False

            elif self.OrderType in [
                order_type.STOP_MKT,
                order_type.STOP_LMT,
                order_type.SNIPER_MKT,
                order_type.SNIPER_LIMIT,
                order_type.TSM,
                order_type.TSL,
            ]:
                se = self.SymbolEnum
                if se < constant.SE_MIN_VALUE or se > constant.SE_MAX_VALUE:
                    self.RejectReason = reject_code.SYMBOL_ENUM_INVALID
                    return False
                if self.StopLimitPrice < constant.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.PRICE_INVALID
                    return False

                if self.OrigOrderID < constant.ORDER_MIN_PRICE:
                    self.RejectReason = reject_code.ORIG_PRICE_INVALID
                    return False

                side = self.BOSide
                if side < 1 or side > 3:
                    self.RejectReason = reject_code.ORDER_SIDE_INVALID
                    return False

                if self.Account <= 0:
                    self.RejectReason = reject_code.ACCOUNT_INVALID
                    return False

                if self.OrderID <= 0:
                    self.RejectReason = reject_code.ORDERID_INVALID
                    return False

                if self.SendingTime <= 0:
                    self.RejectReason = reject_code.SENDING_TIME_INVALID
                    return False


def create_base_message():
    message = Message()
    return message
