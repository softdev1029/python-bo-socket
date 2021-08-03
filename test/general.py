"""
general class for testing. Here are definitions of all tests. tests with name start with 'step' are sequentional
"""
import time
import unittest
import sys
sys.path.append('..')

from constant import order_type
from constant import tif_type, side_type
import traceback

from constant import message_type, symbol_enum, order_message_type, attribute_type
from constant.attribute_type import get_attributes
from helper.logger import logs

logs.set_file_name(__file__)


def wait_for_response(conn, delay=10, errors='raise'):
	"""
	method to wait for response from server
	:param conn:
	:param delay:
	:param errors:
	:return:
	"""
	login_count = 0
	while conn.get_response is False:
		time.sleep(0.5)
		login_count += 0.5
		if login_count > delay:
			if errors == 'raise':
				raise Exception(f'Could not get response in {delay} sec.')
			elif errors == 'ignore':
				logs.info(f'Could not get response in {delay} sec. Ignore')
			break


class OrdersTests(unittest.TestCase):

	orderID = []
	conn = None
	btcequity = []
	symbol = 'BTCUSDT'

	def instrument_request_test(self):
		"""
		instrument specification request test
		:return:
		"""
		self.login()
		data = dict()
		data['BOSymbol'] = self.symbol
		self.conn.write_msg(message_type.MSG_INSTRUMENT_REQUEST, data=data)
		wait_for_response(self.conn, 10, errors='raise')
		for msg in self.conn.messages:
			res = msg.receive_data

			self.assertEqual(res['SymbolEnum'], symbol_enum.DICT[self.symbol])
			self.assertEqual(res["PriceIncrement"], 0.010000)
			self.assertEqual(res["MaxSize"], 5000.000000)
			self.assertEqual(res["MinSize"], 0.000010)

	def login_logout_test(self):
		"""
		logout test
		:return:
		"""
		self.login()
		self.conn.write_msg(message_type.MSG_CLIENT_LOGOUT)
		wait_for_response(self.conn, 10)

		self.conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
		wait_for_response(self.conn, 10)

		res = self.conn.messages[-1].receive_data
		self.assertIn('RejectReason', res)
		logs.info('RejectReason', res['RejectReason'])

	def login(self):
		"""
		logon
		:return:
		"""
		self.conn.write_msg(message_type.MSG_CLIENT_LOGON)
		wait_for_response(self.conn, 10)

	def step2(self, order_type_msg: str, side=side_type.SELL):
		"""
		cancel orders that in the OB
		:return:
		"""
		data = dict()
		data['BOSymbol'] = self.symbol
		data['BOPrice'] = 30001
		data['BOOrderQty'] = 2
		data['BOSide'] = side
		data['TIF'] = tif_type.GTC
		data['MessageType'] = order_message_type.ORDER_NEW
		data['OrderType'] = order_type_msg
		data['OrigOrderID'] = None
		data['StopLimitPrice'] = 20001
		data['Layers'] = 5
		data['SizeIncrement'] = 4
		data['PriceIncrement'] = 2
		data['PriceOffset'] = 1

		data['DisplaySize'] = 0.25
		data['RefreshSize'] = 0.5

		if order_type_msg == order_type.HIDDEN:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE, attribute_type.HIDDEN_TYPE)
		else:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE)

		self.conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
		wait_for_response(self.conn, 3, errors='ignore')

		msgs = []
		for msg in self.conn.messages:
			if msg.receive_data['msg1'] != message_type.MSG_NEW_ORDER['header']:
				continue
			msgs.append(msg.receive_data)

		for msg in msgs:
			if msg['msg1'] != message_type.MSG_NEW_ORDER['header']:
				continue

			msg['MessageType'] = order_message_type.ORDER_CANCEL
			msg['OrigOrderID'] = msg['OrderID']
			msg['OrderID'] = None
			self.conn.write_msg(message_type.MSG_NEW_ORDER,
			                    data=msg)

			wait_for_response(self.conn, 10)

			response = self.conn.messages[-1].receive_data
			if 'RejectReason' in response:
				raise Exception(f'Cancel order rejected: {response["RejectReason_text"]}')

		self.conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
		wait_for_response(self.conn, 10)

		res = self.conn.messages[-1].receive_data
		self.btcequity.append(res['BTCEquity'])

	def step3(self, order_type_msg: str, side=side_type.SELL, error='raise'):
		"""
		put limit order
		:return:
		"""
		data = dict()
		data['BOSymbol'] = self.symbol
		data['BOPrice'] = 30001
		data['BOOrderQty'] = 2
		data['BOSide'] = side
		data['TIF'] = tif_type.GTC
		data['MessageType'] = order_message_type.ORDER_NEW
		data['OrderType'] = order_type_msg
		data['OrigOrderID'] = None
		data['StopLimitPrice'] = 20001
		data['Layers'] = 5
		data['SizeIncrement'] = 4
		data['PriceIncrement'] = 2
		data['PriceOffset'] = 1

		data['DisplaySize'] = 0.25
		data['RefreshSize'] = 0.5

		if order_type_msg == order_type.HIDDEN:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE, attribute_type.HIDDEN_TYPE)
		else:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE)

		self.conn.write_msg(message_type.MSG_NEW_ORDER,
		                    data=data)

		wait_for_response(self.conn, 10)
		res = self.conn.messages[-1].receive_data
		self.orderID.append(res['OrderID'])

		self.conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
		wait_for_response(self.conn, 10)

		self.conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
		wait_for_response(self.conn, 3, errors=error)

		if error == 'raise':

			res = self.conn.messages[-1].receive_data

			self.assertEqual(res['BOPrice'], data['BOPrice'])
			self.assertEqual(res['BOOrderQty'], data['BOOrderQty'])
			self.assertEqual(res['BOSide'], data['BOSide'])
			self.assertEqual(res['TIF'], data['TIF'])
			self.assertEqual(res['BOSymbol'], data['BOSymbol'])

	def step4(self, order_type_msg: str, side=side_type.SELL):
		"""
		CENCEL_REPLACE order and check accuracy
		:return:
		"""
		data = dict()
		data['BOSymbol'] = self.symbol
		data['BOPrice'] = 40001
		data['BOOrderQty'] = 3
		data['BOSide'] = side
		data['TIF'] = tif_type.GTC
		data['MessageType'] = order_message_type.CANCEL_REPLACE
		data['OrderType'] = order_type_msg
		data['OrigOrderID'] = self.orderID[-1]
		data['StopLimitPrice'] = 20001
		data['Layers'] = 5
		data['SizeIncrement'] = 4
		data['PriceIncrement'] = 2
		data['PriceOffset'] = 1

		data['DisplaySize'] = 0.25
		data['RefreshSize'] = 0.5

		if order_type_msg == order_type.HIDDEN:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE, attribute_type.HIDDEN_TYPE)
		else:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE)

		self.conn.write_msg(message_type.MSG_NEW_ORDER,
		                    data=data)

		wait_for_response(self.conn, 10)
		res = self.conn.messages[-1].receive_data
		self.orderID.append(res['OrderID'])

		self.conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
		wait_for_response(self.conn, 10)

		self.conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
		wait_for_response(self.conn, 3, errors='raise')

		res = self.conn.messages[-1].receive_data

		self.assertEqual(res['BOPrice'], data['BOPrice'])
		self.assertEqual(res['BOOrderQty'], data['BOOrderQty'])
		self.assertEqual(res['BOSide'], data['BOSide'])
		self.assertEqual(res['TIF'], data['TIF'])
		self.assertEqual(res['BOSymbol'], data['BOSymbol'])

	def step5(self, order_type_msg: str, side=side_type.SELL):
		"""
		CENCEL order and check accuracy
		:return:
		"""
		data = dict()
		data['BOSymbol'] = self.symbol
		data['BOPrice'] = 40001
		data['BOOrderQty'] = 3
		data['BOSide'] = side
		data['TIF'] = tif_type.GTC
		data['MessageType'] = order_message_type.ORDER_CANCEL
		data['OrderType'] = order_type_msg
		data['OrigOrderID'] = self.orderID[-1]
		data['StopLimitPrice'] = 20001
		data['Layers'] = 5
		data['SizeIncrement'] = 4
		data['PriceIncrement'] = 2
		data['PriceOffset'] = 1

		data['DisplaySize'] = 0.25
		data['RefreshSize'] = 0.5

		if order_type_msg == order_type.HIDDEN:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE, attribute_type.HIDDEN_TYPE)
		else:
			data['Attributes'] = get_attributes(attribute_type.DISPLY_TYPE)

		self.conn.write_msg(message_type.MSG_NEW_ORDER,
		                    data=data)

		wait_for_response(self.conn, 10)
		res = self.conn.messages[-1].receive_data
		self.orderID.append(res['OrderID'])

		self.conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
		wait_for_response(self.conn, 10)

		res = self.conn.messages[-1].receive_data
		self.btcequity.append(res['BTCEquity'])

		self.conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
		wait_for_response(self.conn, 3, errors='ignore')

		self.assertEqual(self.btcequity[-2], self.btcequity[-1])

	def step6(self, order_type_msg: str, side=side_type.SELL):
		"""
		put single order to OB
		:param order_type_msg:
		:param side:
		:return:
		"""
		if order_type_msg in [order_type.LMT,
		                       order_type.PEG,
		                       order_type.HIDDEN,
		                       order_type.PEG_HIDDEN,
		                       order_type.OCO]:
			self.step3(order_type_msg, side)

	def step7(self, order_type_msg, side=side_type.SELL):
		"""
		put order which is opposite to order in step6 in order to execute
		:param order_type_msg: str
		:param side: int
		:return:
		"""
		if order_type_msg in [order_type.LMT,
		                      order_type.PEG,
		                      order_type.HIDDEN,
		                      order_type.PEG_HIDDEN,
		                      order_type.OCO]:
			if side == side_type.SELL:
				side = side_type.BUY
			else:
				side = side_type.SELL
			self.step3(order_type_msg, side=side, error='ignore')

			self.conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
			wait_for_response(self.conn, 10)

			res = self.conn.messages[-1].receive_data
			self.btcequity.append(res['BTCEquity'])

			data = dict()
			data['BOSymbol'] = self.symbol

			self.conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
			wait_for_response(self.conn, 3, errors='ignore')

			order_value_left = 0
			for msg in self.conn.messages:
				res = msg.receive_data

				if res['MessageType'] in [order_message_type.QUOTE_FILL_PARTIAL, order_message_type.EXECUTION_PARTIAL]:
					if res['BOSide'] == side_type.SELL:
						order_value_left += res['RemainingQuantity']

			self.assertEqual(self.btcequity[-3], self.btcequity[-1] - order_value_left)

	def _steps(self):
		"""
		internal function which makes tests running in order
		:return:
		"""
		for name in dir(self):  # dir() result is implicitly sorted
			if name.startswith("step"):
				yield name, lambda x, y: getattr(self, name)(x, y)

	def test_steps(self):
		"""
		just run testcases in sequence from step1, step2, ...
		:return:
		"""
		try:
			self.login()

			for order_type_msg in [order_type.LMT,
			                       order_type.STOP_MKT,
			                       order_type.STOP_LMT,
			                       order_type.PEG,
			                       order_type.HIDDEN,
			                       order_type.PEG_HIDDEN,
			                       order_type.OCO,
			                       order_type.ICE,
			                       order_type.SNIPER_MKT,
			                       order_type.SNIPER_LIMIT,
			                       order_type.TSM,
			                       order_type.TSL]:
				for side in [side_type.SELL,
				             side_type.BUY]:
					for name, step in self._steps():
						try:
							step(order_type_msg, side)
						except Exception as e:
							logs.info(traceback.print_exc())
							logs.info("{} failed ({}: {})".format(step, type(e), e))
							self.fail("{} failed ({}: {})".format(step, type(e), e))

		except Exception as e:
			logs.info(traceback.print_exc())
			logs.info("failed ({}: {})".format(type(e), e))
			self.fail("failed ({}: {})".format(type(e), e))
