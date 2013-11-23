# Tcp Chat server

import socket, select

# a client class, which contains a clients username and chat buffer
class client():
	def __init__(self, username):
		self.buffer = []
		self.username = username

# updates all buffers with the recieved message
def update_buffers(message):
	for client in CLIENTS:
		client.buffer.append(message)

# checks for clients with the username 'username'
def client_named(username):
	for client in CLIENTS:
		if client.username == username:
			return true
	return false

# handles new client connection requests. If the first message sent by 
# a client is not 'USERNAME xxxx' where xxxx is a unique username, the
# connection is terminated.
def handle_new_client(server_socket):
	client_socket, addr = server_socket.accept()
	msg = client_socket.recv(RECV_BUFFER)
	if msg.split(' ')[0] == 'USERNAME':
		username = msg.split(' ')[1]
		if client_named(username):
			client_socket.send("username in use")
			client_socket.close()
		else:
			CONNECTIONS.append(client_socket)
			CLIENTS[client_socket.getpeername()] = client(username)
			update_buffers(username + " entered room\n")
			print username + "connected"
	else:
		client_socket.send("bad handshake - no username provided")
		client_socket.close()

# handles messages recieved from clients. If the message does not follow 
# the form of 'MSG xxxx', where xxxx is the intended message, the message 
# is discarded.
def handle_client_message(client_socket):
	username = CLIENTS[client_socket.getpeername()].username
	try:
		data = client_socket.recv(RECV_BUFFER)
		if data.split(' ')[0] == 'MSG'
			msg = username + ': ' + data.replace('MSG ', '', 1)
		# handle buffer/userlist requests here
	except:
		msg = "Client " + username + " is offline")
		sock.close()
		CONNECTIONS.remove(client_socket)
		CLIENTS.remove(client_socket.getpeername())
	print msg
	update_buffers(msg)

if __name__ == "__main__":

	# initialize global connection structures
	CONNECTIONS = []
	CLIENTS = {}

	# server settings
	RECV_BUFFER = 4096
	PORT = 5000
	HOST = "http://localhost"
	MAX_CONNNECTIONS = 10

	# initialize server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((HOST, PORT))
	server_socket.listen(MAX_CONNNECTIONS)
	CONNECTIONS.append(server_socket)
 
	print "Chat server started on port " + str(PORT)
 
 	# listen for sockets ready to be 'recieved' from
	while 1:
		try:
			read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
			for sock in read_sockets:
				if sock == server_socket:
					handle_new_client(sock)
				else:
					handle_client_message(sock)
	 	except KeyboardInterrupt:
			# close server socket on ctrl + C
			server_socket.close()
