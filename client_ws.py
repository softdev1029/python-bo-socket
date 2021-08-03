"""
simple client of using websocket
"""
import time
import asyncio
from constant import order_type
from constant import tif_type, side_type
import traceback

from helper.logger import logs
from constant import message_type, symbol_enum, order_message_type
from ws.connection import Connection


logs.set_file_name(__file__)
conn = Connection("113.197.36.50", 32043)
conn.start()


def wait_for_response(delay=10, errors='raise'):
	login_count = 0
	while conn.get_response is False:
		time.sleep(0.1)
		login_count += 0.1
		if login_count > delay:
			if errors == 'raise':
				raise Exception(f'Could not get response in {delay} sec.')
			elif errors == 'ignore':
				logs.info(f'Could not get response in {delay} sec. Ignore')
			break


symbol = 'BTCUSDT'

global messages

try:
	conn.write_msg(message_type.MSG_CLIENT_LOGON)
	wait_for_response(10)

	data = {}
	data['BOSymbol'] = symbol
	data['BOPrice'] = 30001
	data['BOOrderQty'] = 0.1
	data['BOSide'] = side_type.SELL
	data['TIF'] = tif_type.GTC
	data['MessageType'] = order_message_type.ORDER_NEW
	data['OrderType'] = order_type.PEG
	data['OrigOrderID'] = None
	data['StopLimitPrice'] = 20001
	data['Layers'] = 5
	data['SizeIncrement'] = 4
	data['PriceIncrement'] = 2
	data['PriceOffset'] = 1
	conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
	wait_for_response(3, errors='ignore')

	orderID = []

	conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
	wait_for_response(10)

	conn.write_msg(message_type.MSG_NEW_ORDER, data=data)

	wait_for_response(10)
	if len(conn.messages) > 0:
		orderID.append(conn.messages[-1].receive_data['OrderID'])

	conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
	wait_for_response(3, errors='ignore')

	data['MessageType'] = order_message_type.ORDER_NEW
	data['OrigOrderID'] = orderID[-1]
	data['BOPrice'] = 30001
	data['BOOrderQty'] = 0.1
	data['BOSide'] = side_type.BUY
	conn.write_msg(message_type.MSG_NEW_ORDER, data=data)
	wait_for_response(10)
	orderID.append(conn.messages[-1].receive_data['OrderID'])

	conn.write_msg(message_type.MSG_COLLATERAL_REQUEST)
	wait_for_response(10)

	conn.write_msg(message_type.MSG_OPEN_ORDER_REQUEST, data=data)
	wait_for_response(3, errors='ignore')

except KeyboardInterrupt:
	logs.info("caught keyboard interrupt, exiting")
except Exception as ex:
	logs.info(traceback.print_exc())

finally:
	conn.close()
