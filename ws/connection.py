"""
class for websocket connection
"""
import websocket as wsc
import traceback
import socket
from threading import Thread
import datetime as dt
from copy import deepcopy
from base.process_message import parse_header, is_message_valid

from base.process_message import process_message
from base.create_message import (
								create_message,
								get_all_request_message_types_string,
								is_valid_message_type,
								MESSAGE_TYPES_KEYS
								)

from constant import message_type, order_message_type, symbol_enum, order_type, tif_type, side_type
from helper.logger import logs
from constant.attribute_type import get_attributes_desc


logs.set_file_name(__file__)
stop_threads = False


class Connection:

	message_type = ""

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.messages = []
		self.logonMsg = None
		self.get_response = False
		self.uri = f'ws://{self.host}:{self.port}'
		logs.info("starting connection to", self.uri, " ...")
		self._conn = None

	def _read_msg(self):

		global stop_threads

		while True:
			if stop_threads:
				break
			try:
				try:
					response = self._conn.recv()
				except wsc.WebSocketTimeoutException as err:
					continue
				self.messages = []
				for ret, reason, msg, msg_len in process_message(response):

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

					if message_type_key == message_type.MSG_NEW_ORDER['header']:
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

					self.messages.append(message)

					self.get_response = True

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
					f"{self.uri}:\n{traceback.format_exc()}",
				)

	def write_msg(self,
	              message,
	              data=None):

		msgObj = create_message(message['desc'])
		if message['header'] != message_type.MSG_CLIENT_LOGON['header']:
			msgObj.set_logon_values(self.logonMsg)

		if message['header'] == message_type.MSG_NEW_ORDER['header']:
			msgObj.set(data)

		if message['header'] in (message_type.MSG_RISK_UPDATE_REQUEST['header'],
		                        message_type.MSG_OPEN_ORDER_REQUEST['header']):
			msgObj.set(data)

		if message['header'] == message_type.MSG_NEW_ORDER['header']:
			send_data = {}

			send_data['SymbolEnum_text'] = symbol_enum.INVDICT[msgObj.send_data['SymbolEnum']]

			if 'OrderID' in msgObj.send_data:
				send_data['OrderID_text'] = msgObj.send_data['OrderID']
			if 'OrigOrderID' in msgObj.send_data:
				send_data['OrigOrderID_text'] = msgObj.send_data['OrigOrderID']
			if 'StopLimitPrice' in msgObj.send_data:
				send_data['StopLimitPrice_text'] = msgObj.send_data['StopLimitPrice']
			if 'Layers' in msgObj.send_data:
				send_data['Layers_text'] = msgObj.send_data['Layers']
			if 'SizeIncrement' in msgObj.send_data:
				send_data['SizeIncrement_text'] = msgObj.send_data['SizeIncrement']
			if 'PriceIncrement' in msgObj.send_data:
				send_data['PriceIncrement_text'] = msgObj.send_data['PriceIncrement']
			if 'PriceOffset' in msgObj.send_data:
				send_data['PriceOffset_text'] = msgObj.send_data['PriceOffset']

			if 'DisplaySize' in msgObj.send_data:
				send_data['DisplaySize_text'] = msgObj.send_data['DisplaySize']
			if 'RefreshSize' in msgObj.send_data:
				send_data['RefreshSize_text'] = msgObj.send_data['RefreshSize']

			if 'Attributes' in msgObj.send_data:
				send_data['Attributes_text'] = get_attributes_desc(msgObj.send_data['Attributes'])

			send_data['BOPrice_text'] = msgObj.send_data['BOPrice']
			send_data['BOOrderQty_text'] = msgObj.send_data['BOOrderQty']

			send_data['OrderType_text'] = order_type.INVDICT[msgObj.send_data['OrderType']]
			send_data['BOSide_text'] = side_type.INVDICT[msgObj.send_data['BOSide']]
			send_data['TIF_text'] = tif_type.INVDICT[msgObj.send_data['TIF']]

			send_data['MessageType_text'] = order_message_type.INVDICT[msgObj.send_data['MessageType']]

			print_str = ''
			print_str_orig = ''
			for k, v in send_data.items():
				m = k.split('_')
				if len(m) == 2 and m[1] == 'text':
					print_str += f'{m[0]} : {v}\n'
				elif len(m) == 1:
					print_str_orig += f'{m[0]} : {v}\n'

			logs.info(f'Text sending:', print_str)

		logs.info('Sending:', msgObj.send_data)
		self.get_response = False
		self._conn.send(msgObj.encode(msgObj.send_data))

	def close(self):

		global stop_threads
		stop_threads = True
		self._th.join()
		self._conn.close()

	def start(self):
		wsc.enableTrace(True)
		self._conn = wsc.create_connection(self.uri, sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1), ), timeout=3)
		self._th = Thread(target=self._read_msg)
		self._th.daemon = True
		self._th.start()

