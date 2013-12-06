#!/usr/bin/python

import threading

from storage import *
from tcp_chat_server import *
from web_socket_chat_server import *

TCP_PORT = 15011
WEB_SOCKET_PORT = 15013

storage = Storage()

tcp_server = TCPChatServer(storage, port=TCP_PORT)
ws_server = WebSocketChatServer(storage, port=WEB_SOCKET_PORT)

tcp_thread = threading.Thread(target=TCPChatServer.listen, args=(tcp_server, ))
ws_thread = threading.Thread(target=WebSocketChatServer.start, args=(ws_server, ))

tcp_thread.start()
ws_thread.start()
