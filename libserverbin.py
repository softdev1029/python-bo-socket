import selectors
import struct


class MessageWrapper:
    def __init__(self, selector, sock, addr, msgObj):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = None
        self._send_buffer = None
        self.request = None
        self.msgObj = msgObj

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

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer = data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
                print(sent)
            except BlockingIOError as e:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                print(e)

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self.request is None:
            self.process_request()

    def write(self):
        if self._send_buffer is None:
            self._send_buffer = self.msgObj.binary_data
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

    def process_request(self):
        data = self._recv_buffer
        if self.msgObj.parse_header(data):
            ret = self.msgObj.parse_message(data)
            if not ret:
                print("Not parse message")
            if self.msgObj.binary_data is not None:
                self._set_selector_events_mask("w")
        else:
            print("Not parse header")
