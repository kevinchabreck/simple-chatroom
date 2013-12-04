
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
		elif header == 'GETUSERS':
			self.factory.sendUserList(self)
		elif header == 'USERNAME':
			self.factory.checkName(self, data.replace('USERNAME:','',1))
		else:
			if header == 'PAINT' or header == 'RESET':
				self.factory.updateBuffer(data)
			elif header == 'CHAT':
				user = self.factory.CLIENTS[self]
				data = data.replace('CHAT:','CHAT:'+user+' -> ', 1)
			#self.factory.updateClients(self, data)
			self.factory.updateClients(data)
			


class PaintFactory(WebSocketServerFactory):

	def __init__(self, url):
		WebSocketServerFactory.__init__(self, url)
		self.CONNECTIONS = []
		self.CLIENTS = {}
		self.PAINTBUFFER = []

	def registerConnection(self, client):
		if not client in self.CONNECTIONS:
			print "registered connection " + client.peerstr
			self.CONNECTIONS.append(client)

	def registerClient(self, client, username):
		if not client in self.CLIENTS.keys():
			self.CLIENTS[client] = username
			print "registered client " + username
			#self.updateClients(client, msg)
			msg = 'INFO:{} has joined the chat'.format(username)
			self.updateClients(msg)
			userlist = 'USERS:' + json.dumps(self.CLIENTS.values())
			self.updateClients(userlist)
			#self.CLIENTS[client] = username

	def unregister(self, client):
		if client in self.CONNECTIONS:
			self.CONNECTIONS.remove(client)
			print "unregistered CONNECTION " + client.peerstr
		if client in self.CLIENTS.keys():
			user = self.CLIENTS[client]
			del self.CLIENTS[client]
			print "unregistered CLIENT " + user
			msg = 'INFO:{} has left the chat'.format(user)
			self.updateClients(msg)
			userlist = 'USERS:' + json.dumps(self.CLIENTS.values())
			self.updateClients(userlist)
			#del self.CLIENTS[client]

	#def updateClients(self, client, msg):
	def updateClients(self, msg):
		for c in self.CONNECTIONS:
			c.sendMessage(msg)
			print "update *"+msg+"* sent to " + c.peerstr

	def checkName(self, client, username):
		if ':' in username:
			client.sendMessage('DENIED:invalid character ":"')
		elif username in self.CLIENTS.values():
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

if __name__ == '__main__':
	print 'server is running'
	factory = PaintFactory("ws://localhost:15013")
	factory.protocol = PaintProtocol
	listenWS(factory)
	reactor.run()
