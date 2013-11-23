class ChatClientController():
  def __init__(self, view=None):
    self.view = view
  
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
    print "TODO"

    return ["kevin", "shuchee", "julia"]

  def requestBuffer(self):
    """
    Requests the buffer from the server.

    @return - the buffer from the server.
    """
    print "TODO"

    return [("julia", "Hi Everyone"), ("shuchee", "Hi")]


  def sendMessage(self, message):
    """
    Sends a message to the server.

    @return void?
    """
    print "TODO"

  def establishConnection(self, server, username):
    """
    Establishes a connection with the given server and username.

    @return true if successful, false otherwise.
    """

    print "TODO"
    return True

