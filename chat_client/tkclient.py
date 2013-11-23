#!/usr/bin/env python

import Tkinter as tk
import sys
from chat_client_controller import *

class TKChatClient(tk.Frame):
  def __init__(self, controller, master=None):
    tk.Frame.__init__(self, master)
    self.controller = controller
    self.grid()
    self.createWidgets()

  def updateUsers(self, users_list):
    self.users_window.config(state=tk.NORMAL)
    self.users_window.delete(1.0, tk.END)
    self.users_window.insert(tk.END, users_list)
    self.users_window.config(state=tk.DISABLED)


  def appendMessage(self, message_tuple):
    self.output_window.config(state=tk.NORMAL)
    self.output_window.insert(tk.END, message_tuple)
    self.output_window.config(state=tk.DISABLED)

  def createWidgets(self):
    self.output_window = tk.Text(self, height=30)
    self.output_window.insert(tk.END, "output window")
    self.output_window.config(state=tk.DISABLED)
    self.output_window.after(500, self.controller.updateOutput)
    self.output_window.grid()
    
    self.input_window = tk.Text(self, height=5)
    self.input_window.insert(tk.END, "input window")
    self.input_window.grid()

    self.users_window = tk.Text(self, height=5)
    self.users_window.insert(tk.END, "users window")
    self.users_window.after(500, self.controller.updateUsers)
    self.users_window.config(state=tk.DISABLED)
    self.users_window.grid()


# Main method
if __name__ == "__main__":
  name = sys.argv[1]
  controller = ChatClientController()
  app = TKChatClient(controller)
  controller.view = app
  app.master.title('%s\'s Chat Room' % name)
  app.mainloop()
