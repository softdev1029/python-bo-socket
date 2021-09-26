#!/usr/bin/env python3

from constant.message_type import ORDER_ACK
from base.connection import start_connect_to_server
from base.thread_handler import socket_thread
from example_message import (
    create_client_logon,
    create_client_logout,
)
from base.logger import log

LIB_STATE_SEND_AES_LOGON = "send_aes_logon"
LIB_STATE_SEND_AES_LOGOUT = "send_aes_logout"
LIB_STATE_SEND_OES_LOGON = "send_oes_logon"
LIB_STATE_SEND_OES_LOGOUT = "send_oes_logout"
LIB_STATE_SEND_ORDER = "send_order"
LIB_STATE_EXIT = "exit"


class LibraryManager:
    def __init__(
        self, aes_host, aes_port, api_key, oes_recv_callback, oes_send_callback
    ):
        self.message_type = ""
        self.manage_state = LIB_STATE_SEND_AES_LOGON

        self.aes_host = aes_host
        self.aes_port = aes_port
        self.api_key = api_key
        self.oes_recv_callback = oes_recv_callback
        self.oes_send_callback = oes_send_callback

    def aes_recv_callback(self, ret, reason, msg, msg_len):
        log("Received message: len=", msg_len)
        if ret is False:
            log("Failed Reason:", reason)
            return

        if msg.Data1 == "H":  # logon message
            if msg.LoginStatus == 1:  # success
                log("AES Logon success")

                oes_ip = msg.PrimaryOrderEntryIP.split(":")
                if len(oes_ip) == 2:
                    host = oes_ip[0]
                    port = int(oes_ip[1].rstrip("\x00"))
                    sel = start_connect_to_server(host, port, self.oes_recv_callback)
                    socket_thread(
                        sel, self.manage_state, self.api_key, self.oes_send_callback
                    )

                    self.manage_state = LIB_STATE_SEND_OES_LOGON
                else:
                    log("AES Logon fail, invalid OES IP")
                    self.manage_state = LIB_STATE_EXIT
            elif msg.LoginStatus == 2:  # failure
                log("AES Logon fail")
                msg.print_reject_reason()
                self.manage_state = LIB_STATE_EXIT
        else:
            log("Unexpected message:", msg.Data1)

    def aes_send_callback(self, socket_controller, api_key):
        if self.manage_state == LIB_STATE_SEND_AES_LOGON:
            log("\nSend the AES Logon message\n")
            socket_controller.msgObj = create_client_logon(self.api_key)
            socket_controller.is_send = True
            self.manage_state = "recv_logon"
        elif self.manage_state == LIB_STATE_SEND_OES_LOGOUT:
            log("\nSend the AES Logout message\n")
            socket_controller.msgObj = create_client_logout()
            socket_controller.is_send = True
            self.manage_state = LIB_STATE_EXIT
        else:
            socket_controller.is_send = False

    def oes_recv_callback_wrapper(self, ret, reason, msg, msg_len):
        self.manage_state = self.oes_recv_callback(ret, reason, msg, msg_len)

    def oes_send_callback_wrapper(self, socket_controller, api_key):
        if self.manage_state == LIB_STATE_SEND_AES_LOGON:
            log("\nSend the OES Logon message\n")
            socket_controller.msgObj = create_client_logon(self.api_key)
            socket_controller.is_send = True
            self.manage_state = "recv_logon"
        elif self.manage_state == LIB_STATE_SEND_AES_LOGOUT:
            log("\nSend the OES Logout message\n")
            socket_controller.msgObj = create_client_logout()
            socket_controller.is_send = True
            self.manage_state = LIB_STATE_EXIT
        elif self.manage_state == LIB_STATE_SEND_ORDER:
            self.oes_send_callback(socket_controller, api_key)
        else:
            socket_controller.is_send = False

    def start(self):
        sel = start_connect_to_server(
            self.aes_host, self.aes_port, self.aes_recv_callback
        )
        socket_thread(sel, self.manage_state, self.api_key, self.aes_send_callback)
