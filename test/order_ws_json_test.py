"""
running tests for websocket
"""
import unittest
import sys
sys.path.append('..')

from general import OrdersTests
from ws.connection import Connection


if __name__ == '__main__':
	OrdersTests.conn = Connection("113.197.36.50", 32043)
	OrdersTests.conn.start()

	unittest.main()

	OrdersTests.conn.close()
