#!/usr/bin/env python3

from constant.message_type import CANCEL_REPLACE, CANCELLED, ORDER_ACK, ORDER_NEW, QUOTE_FILL, REPLACED
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

LIB_STATE_EXIT = "exit"

MAX_ORDER = 10

class LibraryManager:
    def __init__(
        self,
        aes_host,
        aes_port,
        api_key,
        user_name,
        account,
        oes_recv_callback,
        oes_send_callback,
    ):
        self.message_type = ""
        self.manage_state = LIB_STATE_SEND_AES_LOGON

        self.aes_host = aes_host
        self.aes_port = aes_port
        self.api_key = api_key
        self.user_name = user_name
        self.account = account
        self.oes_recv_callback = oes_recv_callback
        self.oes_send_callback = oes_send_callback

        self.aes_key = 0
        self.oes_key = 0

        self.counter = 0

    def aes_send_callback(self, socket_controller, aes_key, api_key):
        # log("At send_callback to AES ...")
        # Step 1: Send AES Logon
        if self.manage_state == LIB_STATE_SEND_AES_LOGON:
            log("Send the AES Logon message\n")
            socket_controller.msgObj = create_client_logon(
                self.aes_key, self.api_key, self.user_name, self.account
            )
            socket_controller.is_send = True
            self.manage_state = "recv_logon"
        elif self.manage_state == LIB_STATE_SEND_OES_LOGOUT:
            log("Send the AES Logout message\n")
            socket_controller.msgObj = create_client_logout(self.aes_key)
            socket_controller.is_send = True
            self.manage_state = LIB_STATE_EXIT
        else:
            socket_controller.is_send = False

    def aes_recv_callback(self, ret, reason, msg, msg_len):
        # Step 2: Receive the AES Logon reply
        log("From AES server, Received message: len=", msg_len)
        if ret is False:
            log("Failed Reason:", reason)
            return

        if msg.Data1 == "H":  # logon message
            if msg.LoginStatus == 1:  # success
                log("AES Logon success")

                self.aes_key = int(msg.Key)

                oes_ip = msg.PrimaryOrderEntryIP.split(":")
                if len(oes_ip) == 2:
                    host = oes_ip[0]
                    port = int(oes_ip[1].rstrip("\x00"))
                    log("The OES server is", host, ":", port, "\n")
                    sel = start_connect_to_server(host, port, self.oes_recv_callback)
                    socket_thread(
                        sel,
                        self.manage_state,
                        self.aes_key,
                        self.api_key,
                        self.oes_send_callback_wrapper,
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

    def oes_send_callback_wrapper(self, socket_controller, aes_or_oes_key, api_key):
        log("At send_callback to OES ...")
        # Step 3: Send the OES Logon
        if self.manage_state == LIB_STATE_SEND_OES_LOGON:
            log("Send the OES Logon message\n")
            socket_controller.msgObj = create_client_logon(aes_or_oes_key, self.api_key, self.user_name, self.account)
            socket_controller.is_send = True
            self.manage_state = "recv_logon"
        elif self.manage_state == LIB_STATE_SEND_OES_LOGOUT:
            log("Send the OES Logout message\n")
            socket_controller.msgObj = create_client_logout(aes_or_oes_key)
            socket_controller.is_send = True
            self.manage_state = LIB_STATE_EXIT
        else:
            self.oes_send_callback(socket_controller, self.oes_key, api_key)
            if socket_controller.is_send:
                type = socket_controller.msgObj.MessageType
                if self.counter > MAX_ORDER:
                        socket_controller.is_send = False
                elif type == ORDER_NEW or type == CANCEL_REPLACE:
                    self.counter = self.counter + 1

        if socket_controller.is_send:
            socket_controller.msgObj.print_message()

        log("At sending, Message Counter is", self.counter, "Tx/Rx state is", self.manage_state)

    def oes_recv_callback_wrapper(self, ret, reason, msg, msg_len):
        log("From OES server, Received message: len=", msg_len)
        if ret is False:
            log("Failed Reason:", reason)
            return
            
        # Step 4: Receive the OES Logon reply
        if msg.Data1 == "H":  # logon message
            if msg.LoginStatus == 1:  # success
                log("OES Logon success")
                self.oes_key = int(msg.Key)
            elif msg.LoginStatus == 2:  # failure
                log("OES Logon fail")
                msg.print_reject_reason()
        elif msg.Data1 == "T":  # order message
            if msg.MessageType == ORDER_ACK:
                log("Order replied")
                self.counter = self.counter - 1
            elif msg.MessageType == CANCELLED:
                log("Order cancelled")
                self.counter = self.counter - 1
            elif msg.MessageType == REPLACED:
                log("Order replaced")
                self.counter = self.counter - 1
            elif msg.MessageType == QUOTE_FILL:
                log("Order quote filled")
                self.counter = self.counter - 1
        else:
            log("Unexpected message:", msg.Data1)

        self.manage_state = self.oes_recv_callback(ret, reason, msg, msg_len)
        log("At receiving, Message Counter is", self.counter, "Tx/Rx state is", self.manage_state)

    def start(self):
        log("The AES server is", self.aes_host, ":", self.aes_port, "\n")
        sel = start_connect_to_server(
            self.aes_host, self.aes_port, self.aes_recv_callback
        )
        socket_thread(
            sel, self.manage_state, self.aes_key, self.api_key, self.aes_send_callback
        )
