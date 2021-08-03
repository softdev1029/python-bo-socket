from base.create_message import create_message, get_message_type_from_header
import json
import traceback
from helper.logger import logs
RECV_NO_ERROR = -1
RECV_ERROR_NOT_ENOUGH_HEADER = 0
RECV_ERROR_NOT_ENOUGH_BODY = 1
RECV_ERROR_INVALID_MSG_TYPE = 2
RECV_ERROR_PARSE = 3
RECV_ERROR_UNKNOWN = 4

logs.set_file_name(__file__)


def parse_header(data):
	if 'msg1' in data.keys():
		return data['msg1']
	elif 'MessageType' in data.keys():
		return data['MessageType']
	else:
		raise KeyError('No valid header key name appears in message')


def is_message_valid(data):
	if data is None:
		return False

	return True


def process_message(many_data):

	response = []
	msg_len = len(many_data)
	for data in many_data.replace(b'}{', b'}BREAK{').split(b'BREAK'):
		try:
			_msg = json.loads(data)
		except Exception as ex:
			logs.info('data:', data)
			traceback.print_exc()
			response.append((False, RECV_ERROR_UNKNOWN, None, None))
			continue

		if len(_msg) < 3:
			logs.info("Invalid buffer, length is", len(_msg))
			response.append((False, RECV_ERROR_NOT_ENOUGH_HEADER, None, None))
			continue
		else:
			msg_key = parse_header(_msg)
			msg_type = get_message_type_from_header(msg_key)
			logs.info("\nMessage type is", msg_type)
			logs.info("Buffer size is", len(_msg))
			if msg_type == "":
				logs.info("Invalid message type", msg_key)
				response.append((False, RECV_ERROR_INVALID_MSG_TYPE, None, None))
				continue
			else:

				ret = create_message(msg_type).decode(data)
				if not ret:
					logs.info("Parse error")
					response.append((False, RECV_ERROR_PARSE, None, None))
					continue
				else:

					response.append((True, RECV_NO_ERROR, ret, msg_len))

	return response


