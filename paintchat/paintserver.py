
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import json

clicks = 0;

class PaintProtocol(WebSocketServerProtocol):

	def onOpen(self):
		self.factory.register(self)

	def connectionLost(self, reason):
		WebSocketServerProtocol.connectionLost(self, reason)
		self.factory.unregister(self)

	def onMessage(self, data, binary):
		print data
		if data != 'GETPAINTBUFFER:':
			if data.split(':')[0] != 'CHAT':
				self.factory.updateBuffer(data)
			self.factory.updateClients(data, binary)
		else:
			self.factory.sendPaintBuffer(self)


class PaintFactory(WebSocketServerFactory):

	def __init__(self, url):
		WebSocketServerFactory.__init__(self, url)
		self.clients = []
		self.PAINTBUFFER = []

	def register(self, client):
		if not client in self.clients:
			print "registered client " + client.peerstr
			self.clients.append(client)
			#self.sendPaintBuffer(client)

	def unregister(self, client):
		if client in self.clients:
			print "unregistered client " + client.peerstr
			self.clients.remove(client)

	def updateClients(self, msg, binary):
		for c in self.clients:
			c.sendMessage(msg, binary)
			print "update *"+msg+"* sent to " + c.peerstr

	def updateBuffer(self, msg):
		if msg == 'RESET:':
			self.PAINTBUFFER = []
		else:
			self.PAINTBUFFER.append(msg.replace('PAINT:', ''))
			print 'added ' + msg.replace('PAINT:', '') + ' to buffer'

	def sendPaintBuffer(self, client):
		print 'sending paint buffer'
		client.sendMessage('PAINTBUFFER:' + json.dumps(self.PAINTBUFFER))

if __name__ == '__main__':
	print 'server is running'
	factory = PaintFactory("ws://localhost:15013")
	factory.protocol = PaintProtocol
	listenWS(factory)
	reactor.run()
