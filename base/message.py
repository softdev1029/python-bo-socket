from constant import constant, reject_code, message_type, order_type, attribute


class Message:
    def __init__(self):
        self.data = ()
        self.binary_data = None

        self.Data1 = None
        self.Data2 = None
        self.MessageLen = None
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

    def parse_message(self, data):
        return self.decode(data)

    def print_reject_reason(self):
        print("Reject Code: ", self.RejectReason)
        msg = "Reject Reason: "
        if self.RejectReason == reject_code.ORDER_NOT_FOUND:
            msg += "ORDER_NOT_FOUND"
        elif self.RejectReason == reject_code.USER_NOT_FOUND:
            msg += "USER_NOT_FOUND"
        elif self.RejectReason == reject_code.ACCOUNT_NOT_FOUND:
            msg += "ACCOUNT_NOT_FOUND"
        elif self.RejectReason == reject_code.INVALID_KEY:
            msg += "INVALID_KEY"
        elif self.RejectReason == reject_code.ACCOUNT_DISABLED:
            msg += "ACCOUNT_DISABLED"
        elif self.RejectReason == reject_code.TRADING_SESSION_INVALID:
            msg += "TRADING_SESSION_INVALID"
        elif self.RejectReason == reject_code.RISK_ACCOUNT_NOT_FOUND:
            msg += "RISK_ACCOUNT_NOT_FOUND"
        elif self.RejectReason == reject_code.RISK_SYMBOL_NOT_FOUND:
            msg += "RISK_SYMBOL_NOT_FOUND"
        elif self.RejectReason == reject_code.MES_NOT_AVAILABLE_TRADING_DISABLED:
            msg += "MES_NOT_AVAILABLE_TRADING_DISABLED"
        elif self.RejectReason == reject_code.OES_NOT_AVAILABLE_TRADING_DISABLED:
            msg += "OES_NOT_AVAILABLE_TRADING_DISABLED"
        elif self.RejectReason == reject_code.MDS_NOT_AVAILABLE_TRADING_DISABLED:
            msg += "MDS_NOT_AVAILABLE_TRADING_DISABLED"
        elif self.RejectReason == reject_code.MSG_TYPE_INVALID:
            msg += "MSG_TYPE_INVALID"
        elif self.RejectReason == reject_code.ORD_TYPE_INVALID:
            msg += "ORD_TYPE_INVALID"
        elif self.RejectReason == reject_code.PRICE_INVALID:
            msg += "PRICE_INVALID"
        elif self.RejectReason == reject_code.SIZE_INVALID:
            msg += "SIZE_INVALID"
        elif self.RejectReason == reject_code.STOP_PRICE_INVALID:
            msg += "STOP_PRICE_INVALID"
        elif self.RejectReason == reject_code.STOP_SIZE_INVALID:
            msg += "STOP_SIZE_INVALID"
        elif self.RejectReason == reject_code.ORDER_SIDE_INVALID:
            msg += "ORDER_SIDE_INVALID"
        elif self.RejectReason == reject_code.ACCOUNT_INVALID:
            msg += "ACCOUNT_INVALID"
        elif self.RejectReason == reject_code.ORDERID_INVALID:
            msg += "ORDERID_INVALID"
        elif self.RejectReason == reject_code.SENDING_TIME_INVALID:
            msg += "SENDING_TIME_INVALID"
        elif self.RejectReason == reject_code.ORIG_PRICE_INVALID:
            msg += "ORIG_PRICE_INVALID"
        elif self.RejectReason == reject_code.ORIG_SIZE_INVALID:
            msg += "ORIG_SIZE_INVALID"
        elif (
            self.RejectReason
            == reject_code.ICE_SIZEINCREMENT_TIMES_LAYERS_NOT_EQUAL_ORDQTY
        ):
            msg += "ICE_SIZEINCREMENT_TIMES_LAYERS_NOT_EQUAL_ORDQTY"
        elif self.RejectReason == reject_code.ORIG_ORDER_ID_INVALID:
            msg += "ORIG_ORDER_ID_INVALID"
        elif self.RejectReason == reject_code.SYMBOL_ENUM_INVALID:
            msg += "SYMBOL_ENUM_INVALID"
        elif self.RejectReason == reject_code.SIZE_INCREMENT_INVALID:
            msg += "SIZE_INCREMENT_INVALID"
        elif self.RejectReason == reject_code.PRICE_OFFSET_INVALID:
            msg += "PRICE_OFFSET_INVALID"
        elif self.RejectReason == reject_code.PRICE_INCREMENT_INVALID:
            msg += "PRICE_INCREMENT_INVALID"
        elif self.RejectReason == reject_code.EXCEEDED_MAX_LAYERS:
            msg += "EXCEEDED_MAX_LAYERS"
        elif self.RejectReason == reject_code.DISPLAY_SIZE_INVALID:
            msg += "DISPLAY_SIZE_INVALID"
        elif self.RejectReason == reject_code.REFRESH_SIZE_INVALID:
            msg += "REFRESH_SIZE_INVALID"
        elif self.RejectReason == reject_code.INVALID_SECURITY_KEY:
            msg += "INVALID_SECURITY_KEY"
        elif self.RejectReason == reject_code.USER_ALREADY_LOGGED_IN:
            msg += "USER_ALREADY_LOGGED_IN"
        elif self.RejectReason == reject_code.INVALID_FIELD_VALUE:
            msg += "INVALID_FIELD_VALUE"
        elif (
            self.RejectReason
            == reject_code.PERCENTAGE_MOVE_EXCEEDED_COOLING_OFF_PERIOD_IN_FORCE
        ):
            msg += "PERCENTAGE_MOVE_EXCEEDED_COOLING_OFF_PERIOD_IN_FORCE"
        elif (
            self.RejectReason == reject_code.INSTRUMET_WOULD_CAUSE_MARGIN_TO_BE_EXCEEDED
        ):
            msg += "INSTRUMET_WOULD_CAUSE_MARGIN_TO_BE_EXCEEDED"
        elif self.RejectReason == reject_code.INSTRUMENT_MARGIN_EXCEEDED:
            msg += "INSTRUMENT_MARGIN_EXCEEDED"
        elif self.RejectReason == reject_code.MARGIN_BUY_ORDER_CANCELLATION_IN_PROGRESS:
            msg += "MARGIN_BUY_ORDER_CANCELLATION_IN_PROGRESS"
        elif (
            self.RejectReason == reject_code.MARGIN_SELL_ORDER_CANCELLATION_IN_PROGRESS
        ):
            msg += "MARGIN_SELL_ORDER_CANCELLATION_IN_PROGRESS"
        elif (
            self.RejectReason
            == reject_code.MARGIN_LONG_POSITION_LIQUIDATION_IN_PROGRESS
        ):
            msg += "MARGIN_LONG_POSITION_LIQUIDATION_IN_PROGRESS"
        elif (
            self.RejectReason
            == reject_code.MARGIN_SHORT_POSITION_LIQUIDATION_IN_PROGRESS
        ):
            msg += "MARGIN_SHORT_POSITION_LIQUIDATION_IN_PROGRESS"
        elif self.RejectReason == reject_code.OUTSTANDING_OPEN_REQUESTS_EXCEEDED:
            msg += "OUTSTANDING_OPEN_REQUESTS_EXCEEDED"
        elif self.RejectReason == reject_code.NO_RISK_DATA:
            msg += "NO_RISK_DATA"
        elif self.RejectReason == reject_code.DUPLICATE_ORDER_ID:
            msg += "DUPLICATE_ORDER_ID"
        elif self.RejectReason == reject_code.EXCEEDS_OPEN_ORDER_REQUESTS:
            msg += "EXCEEDS_OPEN_ORDER_REQUESTS"
        elif self.RejectReason == reject_code.NOT_ENOUGH_EQUITY_TO_COMPLETE:
            msg += "NOT_ENOUGH_EQUITY_TO_COMPLETE"
        elif self.RejectReason == reject_code.MATCHING_ENGINE_REJECTED:
            msg += "MATCHING_ENGINE_REJECTED"
        elif self.RejectReason == reject_code.NONE:
            msg += "NONE"
        elif self.RejectReason == reject_code.ACCEPTED:
            msg += "ACCEPTED"
        elif self.RejectReason == reject_code.KEY_INVALID:
            msg += "KEY_INVALID"
        elif self.RejectReason == reject_code.MSG_SEQ_NUM_INVALID:
            msg += "MSG_SEQ_NUM_INVALID"
        elif self.RejectReason == reject_code.USER_ALREADY_LGGGED_IN:
            msg += "USER_ALREADY_LGGGED_IN"
        elif self.RejectReason == reject_code.ORIG_ORDER_NOT_FOUND:
            msg += "ORIG_ORDER_NOT_FOUND"
        elif self.RejectReason == reject_code.USER_ALREADY_LGGGED_IN:
            msg += "USER_ALREADY_LGGGED_IN"
        elif self.RejectReason == reject_code.INVALID_LOGON_TYPE:
            msg += "INVALID_LOGON_TYPE"
        elif self.RejectReason == reject_code.CANT_EXECUTE_AGAINST_EXCHANGE_ORDER:
            msg += "CANT_EXECUTE_AGAINST_EXCHANGE_ORDER"
        elif self.RejectReason == reject_code.NO_MARKET_MAKER_VOLUME:
            msg += "NO_MARKET_MAKER_VOLUME"
        else:
            msg += "UNKNOWN_REJCT"
        print(msg)

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

                elif self.RejectReason <= 0:
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
        return True


def create_base_message():
    message = Message()
    return message
