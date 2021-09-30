from base.create_message import create_message, get_message_type_from_header
from base.on_message import onMessage
from base.logger import log

RECV_NO_ERROR = -1
RECV_ERROR_NOT_ENOUGH_HEADER = 0
RECV_ERROR_NOT_ENOUGH_BODY = 1
RECV_ERROR_INVALID_MSG_TYPE = 2
RECV_ERROR_PARSE = 3
RECV_ERROR_UNKNOWN = 4


def parse_header(data):
    return (chr(data[0]), data[2] + data[3] * 256)


def process_message(aes_or_oes_key, data):
    log("Processing the received message ...")
    if len(data) < 3:
        log("Invalid buffer, length is", len(data))
        return (False, RECV_ERROR_NOT_ENOUGH_HEADER, None, None)
    else:
        (msg_key, msg_len) = parse_header(data)
        if len(data) < msg_len:
            log(
                "Invalid buffer, length is",
                len(data),
                "requied len is",
                msg_len,
            )
            return (False, RECV_ERROR_NOT_ENOUGH_BODY, None, None)
        else:
            msg_type = get_message_type_from_header(msg_key)
            log("Message type is", msg_type)
            log("Buffer size is", len(data), "required len is", msg_len)
            if msg_type == "":
                log("Invalid message type", msg_key)
                return (False, RECV_ERROR_INVALID_MSG_TYPE, None, None)
            else:
                msg = create_message(aes_or_oes_key, msg_type)
                parsing_data = data[:msg_len]

                ret = msg.parse_message(parsing_data)
                if not ret:
                    log("Parse error")
                    return (False, RECV_ERROR_PARSE, None, None)
                else:
                    onMessage(msg)
                    return (True, RECV_NO_ERROR, msg, msg_len)
    return (False, RECV_ERROR_UNKNOWN)
