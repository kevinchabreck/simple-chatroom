#!/usr/bin/env python
# Tcp Chat server

import socket, select, json, sys

class TCPChatServer():
	def __init__(self, storage, 
			port=15011, host="localhost", max_connections=10):

		# initialize global connection structures
		CONNECTIONS = []
		self.storage = storage

		# server settings
		RECV_BUFFER = 4096

		# initialize server
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# allows socket to be reused in TIME_WAIT state. Do not use in production
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((host, port))
		server_socket.listen(max_connections)
		CONNECTIONS.append(server_socket)

	def listen(self):

		print "Chat server started on port " + str(PORT)

		# listen for sockets ready to be 'recieved' from
		while 1:
			try:
				read_sockets,write_sockets,error_sockets = select.select(CONNECTIONS,[],[])
				for sock in read_sockets:
					if sock == server_socket:
						handle_connection(sock)
					elif sock in CLIENTS.keys():
						handle_client(sock)

			except socket.error:
				if "sock" in vars() and sock in self.storage.clients.keys():
					update_buffers(self.storage.get_client(sock).username + " left the room")
					CONNECTIONS.remove(sock)
					self.storage.remove_client(sock)
					sock.close()

			except KeyboardInterrupt:
				# close server socket on ctrl + C
				print '\nclosing server'
				server_socket.close()
				print 'server closed'
				sys.exit()

	# handles new client connection requests. If the first message sent by
	# a client is not 'USERNAME xxxx' where xxxx is a unique username, the
	# connection is terminated.
	def handle_connection(self, server_socket):
		print 'new connection'
		client_socket, addr = server_socket.accept()
		msg = client_socket.recv(RECV_BUFFER)
		if msg.split(':')[0] == 'USERNAME':
			username = msg.split(':')[1]
			if client_named(username):
				client_socket.send("username in use")
				client_socket.close()
			else:
				CONNECTIONS.append(client_socket)
				self.storage.add_client(client_socket, username)
				self.storage.update_buffers(username + " entered room")
				client_socket.send("connected")
				print username + " connected"
		else:
			client_socket.send("bad handshake - no username provided")
			client_socket.close()

	# handles messages recieved from clients. If the message does not follow
	# the form of 'MSG xxxx', where xxxx is the intended message, the message
	# is discarded.
	def handle_client(self, client_socket):
		print 'handling client'
		username = self.storage.get_client(client_socket).username
		data = client_socket.recv(RECV_BUFFER)
		type = data.split(':')[0]
		if type == 'PUT':
			getMessage(username, data)
		elif type == 'CPUT':
			getCanvasMessage(username, data)
		elif type == 'GET':
			sendBuffer(client_socket)
		elif type == 'CGET':
			sendCanvasBuffer(client_socket)
		elif type == 'FILE':
			getMessage(username, data)
		elif type == 'USERS':
			sendUsers(client_socket)
		else:
			client_socket.send('bad request\nREQUEST: \n' + data)

	def getMessage(self, username, data):
		msg = username + ': ' + data.replace('PUT:', '', 1)
		print msg
		self.storage.update_buffers(msg)

	def getCanvasMessage(self, username, data):
		msg = data.replace('CPUT:', '', 1)
		self.storage.update_canvas_buffers(msg)

	def sendBuffer(self, client_socket):
		client = self.storage.get_client(client_socket)
		buffer = client.buffer
		client_socket.send(json.dumps(buffer))
		client.reset_buffer()

	def sendCanvasBuffer(self, client_socket):
		client = self.storage.get_client(client_socket)
		canvas_buffer = client.canvas_buffer
		client_socket.send(json.dumps(canvas_buffer))
		client.reset_canvas_buffer()
		
	def sendUsers(self, client_socket):
		users = self.storage.client_names()
		client_socket.send(json.dumps(users))


