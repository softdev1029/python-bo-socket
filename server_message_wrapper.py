from base.create_message import create_message, get_message_type_from_header
from base.message_wrapper import MessageWrapper


class ServerMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ServerMessageWrapper, self).__init__(sel, sock, addr, msgObj)

        self._response_created = None

    def read(self):
        self._read()

        ret = True
        while len(self._recv_buffer) > 0 and ret:
            ret = self.process_request()
        self._recv_buffer = b""

    def write(self):
        if self._send_buffer is None:
            self._send_buffer = self.msgObj.binary_data
            self._write()

    def process_request(self):
        data = self._recv_buffer
        if len(data) < 3:
            print("Invalid buffer, length is", len(data))
        else:
            (msg_key, msg_len) = self.parse_header(data)
            if len(data) < msg_len:
                print(
                    "Invalid buffer, length is",
                    len(data),
                    "requied len is",
                    msg_len,
                )
            else:
                msg_type = get_message_type_from_header(msg_key)
                if msg_type == "":
                    print("Invalid message type", msg_key)
                else:
                    self.msgObj = create_message(msg_type)

                    ret = self.msgObj.parse_message(data)
                    if not ret:
                        print("Not parse message")
                    else:
                        self._recv_buffer = self._recv_buffer[msg_len:]
                        return True
                    # if self.msgObj.binary_data is not None:
                    #     self._set_selector_events_mask("w")
        return False
