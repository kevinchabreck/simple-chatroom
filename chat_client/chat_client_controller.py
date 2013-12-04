#!/usr/bin/env python
import socket
import sys
import json

def calls_socket(function):
  def inner(*args):
    try:
      return function(*args)
    except socket.error, e:
      args[0].view.connection_lost()
      args[0].socket.close()
  return inner

class ChatClientController():
  # NOTE: expecting the name to come from instantiation of 
  # this class from tkinter.py file
  def __init__(self, name, view=None):
    self.username    = name
    self.view        = view
    self.RECV_BUFFER = 4096
    self.socket      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(2)
    # NOTE: change the host and port accordingly, i.e this 
    # should be the same as the one used @ server side
    self.establishConnection('127.0.0.1', 5000)

  def updateOutput(self):
    """
    Appends to the output list.

    @return void
    """
    print "Requesting Buffer"
    buf = self.requestBuffer()
    for message in buf:
      print message
      self.view.appendMessage(message)

  def updateUsers(self):
    """
    Refreshes the users list.

    @return void
    """
    users = self.requestUsers()
    self.view.updateUsers(users)

  @calls_socket
  def requestUsers(self):
    """
    Requests the users list from the server.

    @return - the list of users
    """
    # NOTE: assumin that the server will parse the request to 
    # get users in the format USERS:
    self.socket.send('USERS:')
    # NOTE: assuming that the list of users returned from the server 
    # is in the format username1 username2
    # NOTE: well to have spaces differentiate between usernames is a 
    # really bad assumption :) should rather use a format like json
    users = self.socket.recv(self.RECV_BUFFER)
    try:
      users = json.loads(users)
    except:
      pass
    print "Users: " + str(users)
    return users

  @calls_socket
  def requestBuffer(self):
    """
    Requests the buffer from the server.

    @return - the buffer from the server.
    """
    # NOTE: assuming that the server will parse the request to get 
    # messages in the format GET:
    self.socket.send('GET:')
    # NOTE: assuming the server will return messages in this format 
    # username: message
    reqBuff = self.socket.recv(self.RECV_BUFFER)
    try:
      reqBuff = json.loads(reqBuff)
    except:
      pass

    print "Buffer: " + str(reqBuff)
    return reqBuff


  @calls_socket
  def sendMessage(self, message):
    """
    Sends a message to the server.

    @return void
    """
    # NOTE: this method should be called from the tkinter.py file 
    # after the user submits a message from the message window
    # NOTE: assuming that the server will parse the message in this 
    # format PUT:message
    self.socket.send('PUT:' + message)

  def establishConnection(self, server, port):
    """
    Establishes a connection with the given server and username.

    @return true if successful, false otherwise.
    """
    try :
        self.socket.connect((server, port))
        # lets send the username to the server so server can tell us 
        # whether we can start the chat or not
        # NOTE: assuming that the server will parse username in this 
        # format USERNAME:username
        self.socket.send('USERNAME:' + self.username)
        connMsg = self.socket.recv(self.RECV_BUFFER)
        # NOTE: assuming that the server will return a message 'true' 
        # for a successful conn based on a unique username
        if 'connected' not in connMsg:
            print connMsg
            sys.exit()
    except Exception, e:
        print 'Unable to connect', str(e)
        sys.exit()
    return True

  def close(self):
    self.socket.close()
