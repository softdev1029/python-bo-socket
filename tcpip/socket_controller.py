"""
auxilary function to TCPIP socket connection
"""
import selectors
import json
from base.process_message import process_message
from helper.logger import logs


class SocketController:
	def __init__(self, sel, sock, addr, msgObj):
		self.selector = sel
		self.sock = sock
		self.addr = addr

		self._recv_buffer = b""
		self._send_buffer = b""

		self.msgObj = msgObj
		self.response = []
		self.is_send = False

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
			logs.info("\nsending", len(self._send_buffer), "bytes to", self.addr, " ...\n")
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

		self.response = []
		need_read = True

		while need_read:
			recv_len = self._read()
			if recv_len == 0:
				logs.info("No more receive data\n")

			need_read = recv_len > 0

			ret = need_read
			while ret:
				response = process_message(self._recv_buffer)
				self.response.extend(response)
				ret, reason, msg, msg_len = response[-1]
				if ret:
					self._recv_buffer = self._recv_buffer[msg_len:]
					if self._recv_buffer == b'':
						ret = False

		# here, _recv_buffer should be empty
		# otherwise, we need to check reason
		self._recv_buffer = b""

	def write(self):
		if self.is_send:
			self.queue_request()

		self._write()

	def close(self):
		logs.info("closing connection to", self.addr)
		try:
			self.selector.unregister(self.sock)
		except Exception as e:
			logs.info(
				"error: selector.unregister() exception for",
				f"{self.addr}: {repr(e)}",
			)

		try:
			self.sock.close()
		except OSError as e:
			logs.info(
				"error: socket.close() exception for",
				f"{self.addr}: {repr(e)}",
			)
		finally:
			# Delete reference to socket object for garbage collection
			self.sock = None

	def queue_request(self):

		self._send_buffer = self.msgObj.encode(self.msgObj.send_data)
		_len_buffer = {'Len': len(self._send_buffer)}
		self._send_buffer = self.msgObj.encode(_len_buffer) + self._send_buffer


