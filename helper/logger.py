"""
logging module
"""
import logging
import datetime as dt
import os


class Logger:

	def __init__(self):
		logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(name)-20s] [%(levelname)-5.5s]  %(message)s")
		self.rootLogger = logging.getLogger()
		self.rootLogger.setLevel(logging.DEBUG)
		self.set_file_name('logger')
		logPath = './logs'
		os.makedirs(logPath, exist_ok=True)
		fileName = f'bit24_api_{dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'
		fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
		fileHandler.setFormatter(logFormatter)
		self.rootLogger.addHandler(fileHandler)
		consoleHandler = logging.StreamHandler()
		consoleHandler.setFormatter(logFormatter)
		self.rootLogger.addHandler(consoleHandler)

	def set_file_name(self, name):
		self.rootLogger.name = name

	def info(self, msg, *args):
		"""
		main logging function. Behaviour like print, means one can put arguments splitted by coma
		:param msg:
		:param args:
		:return:
		"""
		if len(args) > 0:
			self.rootLogger.debug('  '.join([str(m) if not isinstance(m, str) else m for m in [msg, *args]]))
		else:
			self.rootLogger.debug(str(msg))

	def error(self, msg, *args):
		if len(args) > 0:
			self.rootLogger.error('  '.join([str(m) if not isinstance(m, str) else m for m in [msg, *args]]))
		else:
			self.rootLogger.error(str(msg))


logs = Logger()
