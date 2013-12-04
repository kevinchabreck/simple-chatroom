
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import json

clicks = 0;

class PaintProtocol(WebSocketServerProtocol):

	def onOpen(self):
		self.factory.registerConnection(self)

	def connectionLost(self, reason):
		WebSocketServerProtocol.connectionLost(self, reason)
		self.factory.unregister(self)

	# possible message headers:
	# PAINT, CHAT, RESET, USERNAME, GETPAINTBUFFER
	def onMessage(self, data, binary):
		print data
		header = data.split(':')[0]
		if header == 'GETPAINTBUFFER':
			self.factory.sendPaintBuffer(self)
		elif header == 'USERNAME':
			self.factory.checkName(self, data.replace('USERNAME:','',1))
		elif self in factory.CLIENTS.keys():
			if header == 'PAINT' or header == 'RESET':
				self.factory.updateBuffer(data)
			elif header == 'CHAT':
				user = self.factory.CLIENTS[self]
				data = data.replace('CHAT:','CHAT:'+user+': ', 1)
			self.factory.updateClients(data)
		else:
			self.sendMessage('DENIED:unregistered user')
			

class PaintFactory(WebSocketServerFactory):

	def __init__(self, url, storage):
		WebSocketServerFactory.__init__(self, url)
		self.CONNECTIONS = []
		self.storage = storage
		self.PAINTBUFFER = []

	def registerConnection(self, client):
		if not client in self.CONNECTIONS:
			print "registered connection " + client.peerstr
			self.CONNECTIONS.append(client)

	def registerClient(self, client, username):
		if not client in self.storage.clients.keys():
			self.storage.add_client(username)
			print "registered client " + username
			msg = 'INFO:{} has joined the chat'.format(username)
			self.updateClients(msg)
			userlist = 'USERS:' + json.dumps(self.storage.client_names())
			self.updateClients(userlist)

	def unregister(self, client):
		if client in self.CONNECTIONS:
			self.CONNECTIONS.remove(client)
			print "unregistered CONNECTION " + client.peerstr
		if client in self.CLIENTS.keys():
			user = self.storage.clients[client]
			self.storage.remove_client(client)
			print "unregistered CLIENT " + user
			msg = 'INFO:{} has left the chat'.format(user)
			self.updateClients(msg)
			userlist = 'USERS:' + json.dumps(self.storage.client_names())
			self.updateClients(userlist)

	def updateClients(self, msg):
		for c in self.CONNECTIONS:
			c.sendMessage(msg)
			print "update *"+msg+"* sent to " + c.peerstr

	def checkName(self, client, username):
		if ':' in username:
			client.sendMessage('DENIED:invalid character ":"')
		elif username.isspace() or username == '':
			client.sendMessage('DENIED:username must have at least one alphanumeric char')
		elif username == 'null' or username == 'undefined':
			client.sendMessage('DENIED:username cannot be null or undefined')
		elif username.lower() in [x.lower() for x in self.CLIENTS.values()]:
			client.sendMessage('DENIED:username in use')
		else:
			self.registerClient(client, username)
			client.sendMessage('ACCEPTED:')

	def updateBuffer(self, msg):
		if msg == 'RESET:':
			self.PAINTBUFFER = []
		else:
			self.PAINTBUFFER.append(msg.replace('PAINT:', ''))
			print 'added ' + msg.replace('PAINT:', '') + ' to buffer'

	def sendPaintBuffer(self, client):
		print 'sending paint buffer'
		client.sendMessage('PAINTBUFFER:' + json.dumps(self.PAINTBUFFER))

	def sendUserList(self, client):
		print 'sending userlist'
		client.sendMessage('USERS:' + json.dumps(self.CLIENTS.values()))		

class WebSocketChatServer():
	def __init__(self, storage, port=15013, host="localhost"):
		self.storage = storage
		print 'server is running'
		factory = PaintFactory("ws://%s:%d" % (host, port), storage)
		factory.protocol = PaintProtocol
		listenWS(factory)

	def start(self):
		reactor.run()
