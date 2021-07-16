from base.process_message import process_message
import selectors


class SocketController:
    def __init__(self, sel, sock, addr, msgObj):
        self.selector = sel
        self.sock = sock
        self.addr = addr

        self._recv_buffer = b""
        self._send_buffer = b""

        self.msgObj = msgObj

        self.is_send = False

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
                self.is_send = False

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        need_read = True

        while need_read:
            recv_len = self._read()
            if recv_len == 0:
                print("No more receive data\n")

            need_read = recv_len > 0

            ret = need_read
            while ret:
                (ret, reason, msg, msg_len) = process_message(self._recv_buffer)
                if ret:
                    self._recv_buffer = self._recv_buffer[msg_len:]

        # here, _recv_buffer should be empty
        # otherwise, we need to check reason
        self._recv_buffer = b""

    def write(self):
        if self.is_send:
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

    def queue_request(self):
        if self.msgObj.encode() is True:
            message = self.msgObj.binary_data
            self._send_buffer += message