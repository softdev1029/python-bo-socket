"""
module responsible for connection by socket TCPIP
"""
import socket
import selectors
import traceback
from threading import Thread
from copy import deepcopy
import datetime as dt

from base.process_message import parse_header, is_message_valid
from tcpip.socket_controller import SocketController

from base.create_message import (
								create_message,
								get_all_request_message_types_string,
								is_valid_message_type,
								MESSAGE_TYPES_KEYS
								)

from constant import message_type, order_message_type, symbol_enum, order_type, tif_type, side_type
from helper.logger import logs
from constant.attribute_type import get_attributes_desc

stop_threads = False
logs.set_file_name(__file__)


class Connection:

	sel = selectors.DefaultSelector()

	message_type = ""

	def __init__(self, host: str, port: int) -> None:
		"""
		main class
		:param host: str
		:param port: int
		"""
		self.host = host
		self.port = port
		self.messages = []
		self.logonMsg = None
		self.get_response = False

	def _start_connection(self) -> None:
		"""
		creating the connection
		:return:
		"""
		addr = (self.host, self.port)
		logs.info("\nstarting connection to", addr, " ...\n")

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setblocking(False)
		sock.connect_ex(addr)

		msgObj = create_message(self.message_type)

		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		socket_controller = SocketController(
			self.sel, sock, addr, msgObj
		)
		self.sel.register(sock, events, data=socket_controller)

	def _read_msg(self) -> None:
		"""
		in loop reading message, when stop_threads == True the loop is breaking
		:return:
		"""
		while True:
			events = self.sel.select(timeout=1)

			for key, mask in events:
				if mask == selectors.EVENT_WRITE:
					continue

				socket_controller = key.data

				self.messages = []

				try:
					socket_controller.process_events(mask)
					for ret, reason, msg, msg_len in socket_controller.response:

						if not is_message_valid(msg):
							continue

						message_type_key = parse_header(msg)
						message = create_message(message_type_key)
						message.set_msg(msg)
						message.receive_data['msg1_text'] = MESSAGE_TYPES_KEYS[message_type_key]
						if 'SendingTime' in msg:
							message.receive_data['SendingTime_text'] = dt.datetime.fromtimestamp(msg['SendingTime'] / 1e9).isoformat()
						if 'RejectReason' in msg:
							message.receive_data['RejectReason_text'] = message.reject_reason_msg(msg['RejectReason'])
						if message_type_key == message_type.MSG_CLIENT_LOGON['header']:
							self.logonMsg = message

						if message_type_key == 'T':
							message.receive_data['SymbolEnum_text'] = symbol_enum.INVDICT[message.receive_data['SymbolEnum']]

							if 'OrderID' in message.receive_data:
								message.receive_data['OrderID_text'] = message.receive_data['OrderID']
							if 'OrigOrderID' in message.receive_data:
								message.receive_data['OrigOrderID_text'] = message.receive_data['OrigOrderID']
							if 'StopLimitPrice' in message.receive_data:
								message.receive_data['StopLimitPrice_text'] = message.receive_data['StopLimitPrice']
							if 'Layers' in message.receive_data:
								message.receive_data['Layers_text'] = message.receive_data['Layers']
							if 'SizeIncrement' in message.receive_data:
								message.receive_data['SizeIncrement_text'] = message.receive_data['SizeIncrement']
							if 'PriceIncrement' in message.receive_data:
								message.receive_data['PriceIncrement_text'] = message.receive_data['PriceIncrement']
							if 'PriceOffset' in message.receive_data:
								message.receive_data['PriceOffset_text'] = message.receive_data['PriceOffset']

							if 'DisplaySize' in message.receive_data:
								message.receive_data['DisplaySize_text'] = message.receive_data['DisplaySize']
							if 'RefreshSize' in message.receive_data:
								message.receive_data['RefreshSize_text'] = message.receive_data['RefreshSize']

							if 'Attributes' in message.receive_data:
								message.receive_data['Attributes_text'] = get_attributes_desc(message.receive_data['Attributes'])

							message.receive_data['BOPrice_text'] = message.receive_data['BOPrice']
							message.receive_data['BOOrderQty_text'] = message.receive_data['BOOrderQty']

							message.receive_data['OrderType_text'] = order_type.INVDICT[message.receive_data['OrderType']]
							message.receive_data['BOSide_text'] = side_type.INVDICT[message.receive_data['BOSide']]
							message.receive_data['TIF_text'] = tif_type.INVDICT[message.receive_data['TIF']]

							message.receive_data['MessageType_text'] = order_message_type.INVDICT[message.receive_data['MessageType']]

						if message_type_key == message_type.MSG_COLLATERAL_RESPONSE['header']:
							for k, v in deepcopy(message.receive_data).items():
								if k.find('Equity') > 0:
									message.receive_data[k + '_text'] = v

						self.get_response = True

						self.messages.append(message)
						logs.info('Response:', message.receive_data)
						print_str = ''
						print_str_orig = ''
						for k, v in message.receive_data.items():
							m = k.split('_')
							if len(m) == 2 and m[1] == 'text':
								print_str += f'{m[0]} : {v}\n'
							elif len(m) == 1:
								print_str_orig += f'{m[0]} : {v}\n'

						# self.log.info(f'Original response:', print_str_orig)
						logs.info(f'Text response:', print_str)

				except Exception:
					logs.info(
						"main: error: exception for",
						f"{socket_controller.addr}:\n{traceback.format_exc()}",
					)
					socket_controller.close()

			global stop_threads
			if stop_threads:
				break

	def _start_read(self):
		"""
		run read in thread
		:return:
		"""
		self._th = Thread(target=self._read_msg)
		self._th.start()

	def write_msg(self,
	              message,
	              data=None) -> None:
		"""
		writing the message to socket. Not in the loop
		:param message: int
		:param data: message.receive_data
		:return:
		"""
		self.get_response = False
		events = self.sel.select(timeout=1)
		for key, mask in events:
			if mask == selectors.EVENT_READ:
				continue

			socket_controller = key.data

			socket_controller.msgObj = create_message(message['desc'])
			if message['header'] != message_type.MSG_CLIENT_LOGON['header']:
				socket_controller.msgObj.set_logon_values(self.logonMsg)

			if message['header'] == message_type.MSG_NEW_ORDER['header']:
				socket_controller.msgObj.set(data)

			if message['header'] in (message_type.MSG_RISK_UPDATE_REQUEST['header'],
			                        message_type.MSG_OPEN_ORDER_REQUEST['header']):
				socket_controller.msgObj.set(data)

			if message['header'] == message_type.MSG_NEW_ORDER['header']:
				send_data = {}

				send_data['SymbolEnum_text'] = symbol_enum.INVDICT[socket_controller.msgObj.send_data['SymbolEnum']]

				if 'OrderID' in socket_controller.msgObj.send_data:
					send_data['OrderID_text'] = socket_controller.msgObj.send_data['OrderID']
				if 'OrigOrderID' in socket_controller.msgObj.send_data:
					send_data['OrigOrderID_text'] = socket_controller.msgObj.send_data['OrigOrderID']
				if 'StopLimitPrice' in socket_controller.msgObj.send_data:
					send_data['StopLimitPrice_text'] = socket_controller.msgObj.send_data['StopLimitPrice']
				if 'Layers' in socket_controller.msgObj.send_data:
					send_data['Layers_text'] = socket_controller.msgObj.send_data['Layers']
				if 'SizeIncrement' in socket_controller.msgObj.send_data:
					send_data['SizeIncrement_text'] = socket_controller.msgObj.send_data['SizeIncrement']
				if 'PriceIncrement' in socket_controller.msgObj.send_data:
					send_data['PriceIncrement_text'] = socket_controller.msgObj.send_data['PriceIncrement']
				if 'PriceOffset' in socket_controller.msgObj.send_data:
					send_data['PriceOffset_text'] = socket_controller.msgObj.send_data['PriceOffset']

				if 'DisplaySize' in socket_controller.msgObj.send_data:
					send_data['DisplaySize_text'] = socket_controller.msgObj.send_data['DisplaySize']
				if 'RefreshSize' in socket_controller.msgObj.send_data:
					send_data['RefreshSize_text'] = socket_controller.msgObj.send_data['RefreshSize']

				if 'Attributes' in socket_controller.msgObj.send_data:
					send_data['Attributes_text'] = get_attributes_desc(socket_controller.msgObj.send_data['Attributes'])

				send_data['BOPrice_text'] = socket_controller.msgObj.send_data['BOPrice']
				send_data['BOOrderQty_text'] = socket_controller.msgObj.send_data['BOOrderQty']

				send_data['OrderType_text'] = order_type.INVDICT[socket_controller.msgObj.send_data['OrderType']]
				send_data['BOSide_text'] = side_type.INVDICT[socket_controller.msgObj.send_data['BOSide']]
				send_data['TIF_text'] = tif_type.INVDICT[socket_controller.msgObj.send_data['TIF']]

				send_data['MessageType_text'] = order_message_type.INVDICT[socket_controller.msgObj.send_data['MessageType']]

				logs.info('Sending:', socket_controller.msgObj.send_data)
				print_str = ''
				print_str_orig = ''
				for k, v in send_data.items():
					m = k.split('_')
					if len(m) == 2 and m[1] == 'text':
						print_str += f'{m[0]} : {v}\n'
					elif len(m) == 1:
						print_str_orig += f'{m[0]} : {v}\n'

				# logs.info(f'Original response:', print_str_orig)
				logs.info(f'Text sending:', print_str)

			socket_controller.is_send = True
			logs.info("\n")

			try:
				socket_controller.process_events(mask)
			except Exception:
				logs.info(
					"main: error: exception for",
					f"{socket_controller.addr}:\n{traceback.format_exc()}",
				)
				socket_controller.close()

	def close(self) -> None:
		"""
		close the connection and get out of read thread
		:return:
		"""
		global stop_threads

		stop_threads = True
		self._th.join()
		self.sel.close()

	def start(self) -> None:
		"""
		main function to run on beginning
		:return:
		"""
		self._start_connection()
		self._start_read()

