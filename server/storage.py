
################################################################################
# CURRENT CLIENTSIDE CONSTRAINTS:
#	1) usernames cannot have any non-alphabetical or non-numerical characters in them
################################################################################


# a client class, which contains a clients username and chat buffer
class Client():
  def __init__(self, username):
    self.buffer = ['welcome to the chat!']
    self.canvas_buffer = []
    self.username = username

  def reset_buffer(self):
    self.buffer = []

  def reset_canvas_buffer(self):
    self.canvas_buffer = []

class Storage():
  def __init__(self):
    self.clients = {}

  def add_client(self, socket, username):
    ""

  def remove_client(self, socket):
    del self.clients[socket]

  def get_client(self, socket):
    ""
  def client_names(self):
    return [c.username for c in self.clients.values()]
    
  def update_canvas_buffers(canvas_message):
    for client in self.clients:
      self.clients[client].canvas_buffer.append(canvas_message)
      


  # updates all buffers with the recieved message
  def update_buffers(message):
    for client in self.clients:
      self.clients[client].buffer.append(message)

  # checks for clients with the username 'username'
  def client_named(username):
    for client in self.clients:
      if self.clients[client].username == username:
        return True
    return False
