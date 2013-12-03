#!/usr/bin/env python
# Tcp Chat server

import socket, select, json

################################################################################
# CURRENT CLIENTSIDE CONSTRAINTS:
#	1) usernames cannot have any non-alphabetical or non-numerical characters in them
################################################################################

# a client class, which contains a clients username and chat buffer
class Client():
	def __init__(self, username):
		self.buffer = ['welcome to the chat!']
		self.username = username

# updates all buffers with the recieved message
def update_buffers(message):
	for client in CLIENTS:
		CLIENTS[client].buffer.append(message)

# checks for clients with the username 'username'
def client_named(username):
	for client in CLIENTS:
		if CLIENTS[client].username == username:
			return True
	return False

# handles new client connection requests. If the first message sent by 
# a client is not 'USERNAME xxxx' where xxxx is a unique username, the
# connection is terminated.
def handle_connection(server_socket):
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
			CLIENTS[client_socket.getpeername()] = Client(username)
			update_buffers(username + " entered room")
			client_socket.send("connected")
			print username + " connected"
	else:
		client_socket.send("bad handshake - no username provided")
		client_socket.close()

# handles messages recieved from clients. If the message does not follow 
# the form of 'MSG xxxx', where xxxx is the intended message, the message 
# is discarded.
def handle_client(client_socket):
	print 'handling client'
	username = CLIENTS[client_socket.getpeername()].username
	try:
		data = client_socket.recv(RECV_BUFFER)
		type = data.split(':')[0]
		if type == 'PUT':
			getMessage(username, data)
		elif type == 'GET':
			sendBuffer(client_socket)
		elif type == 'USERS':
			sendUsers(client_socket)
		else:
			client_socket.send('bad request\nREQUEST: \n' + data)
	except socket.error, e:
		traceback.print_exc
		msg = "Client " + username + " is offline"
		sock.close()
		CONNECTIONS.remove(client_socket)
		del CLIENTS[client_socket.getpeername()]


def getMessage(username, data):
	msg = username + ': ' + data.replace('PUT:', '', 1)
	print msg
	update_buffers(msg)

def sendBuffer(client_socket):
	buffer = CLIENTS[client_socket.getpeername()].buffer
	client_socket.send(json.dumps(buffer))
	CLIENTS[client_socket.getpeername()].buffer = []

def sendUsers(client_socket):
	users = [client.username for client in CLIENTS.values()]
	client_socket.send(json.dumps(users))

if __name__ == "__main__":

	# initialize global connection structures
	CONNECTIONS = []
	CLIENTS = {}

	# server settings
	RECV_BUFFER = 4096
	PORT = 5000
	HOST = "localhost"
	MAX_CONNNECTIONS = 10

	# initialize server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# allows socket to be reused in TIME_WAIT state. Do not use in production
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(MAX_CONNNECTIONS)
	CONNECTIONS.append(server_socket)
 
	print "Chat server started on port " + str(PORT)
 
 	# listen for sockets ready to be 'recieved' from
	while 1:
		try:
			read_sockets,write_sockets,error_sockets = select.select(CONNECTIONS,[],[])
			for sock in read_sockets:
				if sock == server_socket:
					handle_connection(sock)
				elif sock.getpeername() in CLIENTS.keys():
					handle_client(sock)
		
		except socket.error:
			sock.close()
			CONNECTIONS.remove(sock)
			# TODO: remove from CLIENTS

	 	except KeyboardInterrupt:
			# close server socket on ctrl + C
			print '\nclosing server'
			server_socket.close()
			print 'server closed'
