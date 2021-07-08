import selectors
from base.create_message import create_message, get_message_type_from_header

RECV_NO_ERROR = -1
RECV_ERROR_NOT_ENOUGH_HEADER = 0
RECV_ERROR_NOT_ENOUGH_BODY = 1
RECV_ERROR_INVALID_MSG_TYPE = 2
RECV_ERROR_UNKNOWN_PARSE = 3
RECV_ERROR_UNKNOWN = 4


class MessageController:
    def __init__(self, sel, sock, addr, msgObj):
        self.selector = sel
        self.sock = sock
        self.addr = addr

        self._recv_buffer = b""
        self._send_buffer = b""

        self.msgObj = msgObj

        self._request_queued = False

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    # returns the length of received data
    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            return 0
        else:
            if data:
                self._recv_buffer += data
                return len(data)
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print("\nsending", len(self._send_buffer), "bytes to", self.addr, " ...\n")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                self._request_queued = False

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        need_read = True

        while need_read:
            recv_len = self._read()

            need_read = recv_len > 0

            ret = True
            while ret:
                (ret, reason) = self.process_request()

        # here, _recv_buffer should be empty
        # otherwise, we need to check reason

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                "error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def parse_header(self, data):
        return (chr(self._recv_buffer[0]), self._recv_buffer[2])

    def process_request(self):
        data = self._recv_buffer
        if len(data) < 3:
            print("Invalid buffer, length is", len(data))
            return (False, RECV_ERROR_NOT_ENOUGH_HEADER)
        else:
            (msg_key, msg_len) = self.parse_header(data)
            if len(data) < msg_len:
                print(
                    "Invalid buffer, length is",
                    len(data),
                    "requied len is",
                    msg_len,
                )
                return (False, RECV_ERROR_NOT_ENOUGH_BODY)
            else:
                msg_type = get_message_type_from_header(msg_key)
                print("\nMessage type is", msg_type)
                print("Buffer size is", len(data), "required len is", msg_len)
                if msg_type == "":
                    print("Invalid message type", msg_key)
                    return (False, RECV_ERROR_INVALID_MSG_TYPE)
                else:
                    self.msgObj = create_message(msg_type)
                    parsing_data = data[:msg_len]

                    ret = self.msgObj.parse_message(parsing_data)
                    if not ret:
                        print("Not parse message")
                        return (False, RECV_ERROR_UNKNOWN_PARSE)
                    else:
                        self._recv_buffer = self._recv_buffer[msg_len:]
                        return (True, RECV_NO_ERROR)
        return (False, RECV_ERROR_UNKNOWN)

    def queue_request(self):
        if self.msgObj.encode() is True:
            message = self.msgObj.binary_data
            self._send_buffer += message
            self._request_queued = True
