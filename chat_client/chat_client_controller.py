class ChatClientController():
  def __init__(self, socket, view=None):
    '''
       NOTE: make sure tkclient passes the socket param elese declare the socket locally
    '''
    self.socket = socket
    self.view   = view
    self.RECV_BUFFER = 4096

  def updateOutput(self):
    """
    Appends to the output list.

    @return void
    """
    buf = self.requestBuffer()
    for message in buf:
      self.view.appendMessage(message)

  def updateUsers(self):
    """
    Refreshes the users list.

    @return void
    """
    users = self.requestUsers()
    self.view.updateUsers(users)

  def requestUsers(self):
    """
    Requests the users list from the server.

    @return - the list of users
    """
    self.socket.send('USERS:')
    users = self.socket.recv(self.socket.RECV_BUFFER)
    # TODO: should rather be using some msg packing thing here to send and receive messages
    # NOTE: assumed that the list of users returned by the server is a string with spaces to differentiate between the users
    # eg. kevin shuchee julia    is the string returnred by the server when the client asked for 'USERS'
    return users.split()
    #return ["kevin", "shuchee", "julia"]

  def requestBuffer(self):
    """
    Requests the buffer from the server.

    @return - the buffer from the server.
    """
    '''
       NOTE: server should parse out the get request and not display the string get
    '''
    self.socket.send('GET:')
    reqBuf = self.socket.recv(self.RECV_BUFFER)
    '''
       TODO: this has to be a tuple of username and the msg
    '''
    return [('username', reqBuf)]

    #return [("julia", "Hi Everyone"), ("shuchee", "Hi")]


  def sendMessage(self, message):
    """
    Sends a message to the server.

    @return void?
    """
    self.socket.send('PUT:' + message)


  def establishConnection(self, server, port, username):
    # TODO: assumed that the port no. will be provided as the second param to this method
    """
    Establishes a connection with the given server and username.

    @return true if successful, false otherwise.
    """
    self.socket.connect((server, port))
    self.socket.send('USERNAME ' + username)
    # assuming that the server returns a string 'true' on a successful conn
    # if server never returned anything on a successfull conn, then the client will just sit here in limbo mode
    msgFromServer = self.socket.recv(self.RECV_BUFFER)
    if msgFromServer.lower() != 'true':
      print msgFromServer
      return False

    return True
