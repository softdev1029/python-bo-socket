import selectors
import struct


class MessageWrapper:
    def __init__(self, selector, sock, addr, request):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._content_len = None
        self.response = None

    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr, " ...\n")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]

    def _create_message(self, *, content_bytes):
        message_hdr = struct.pack(">H", len(content_bytes))
        message = message_hdr + content_bytes
        return message

    def process_events(self, mask):
        if mask & selectors.EVENT_WRITE:
            self.write()

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

    def queue_request(self):
        content = self.request["content"]
        req = {
            "content_bytes": content,
        }
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True
