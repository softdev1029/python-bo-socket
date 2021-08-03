"""
running test for TCPIP socket
"""
import unittest
import sys
sys.path.append('..')

from general import OrdersTests
from tcpip.connection import Connection


if __name__ == '__main__':
	OrdersTests.conn = Connection("113.197.36.50", 32042)
	OrdersTests.conn.start()

	unittest.main()

	OrdersTests.conn.close()


