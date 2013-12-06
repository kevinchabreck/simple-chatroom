#!/usr/bin/env python

import Tkinter as tk
import tkMessageBox
import sys
from chat_client_controller import *

class TKChatClient(tk.Frame):
  INPUT_LIMIT = 100
  REFRESH_RATE = 1000

  def __init__(self, controller, master=None):
    tk.Frame.__init__(self, master)
    self.controller = controller
    self.grid()
    self.createWidgets()
    self.has_connection = True

  def connection_lost(self):
    title = "Connection Lost"
    message = "Connection to server lost. Closing application."
    self.has_connection = False
    tkMessageBox.showerror(title, message)
    sys.exit()


  def refresh(self):
    if self.has_connection:
      print "Refreshing"
      self.controller.updateOutput()
      self.controller.updateUsers()
      self.after(REFRESH_RATE, self.refresh)


  def updateUsers(self, users_list):
    self.users_window.config(state=tk.NORMAL)
    self.users_window.delete(1.0, tk.END)
    self.users_window.insert(tk.END, ", ".join(users_list))
    self.users_window.config(state=tk.DISABLED)


  def appendMessage(self, message):
    self.output_window.config(state=tk.NORMAL)
    self.output_window.insert(tk.END, message + "\n")
    self.output_window.config(state=tk.DISABLED)


  def messageSendEventHandler(self, event):
    message = self.input_window.get(1.0, tk.END).strip()
    print "Sending message: '%s'" % message
    self.input_window.delete(1.0, tk.END)
    self.input_window_chars = 0
    self.controller.sendMessage(message)

  def messageLimitSizeHandler(self, event):
    print "Testing limiting"
    message = self.input_window.get(1.0, tk.END).strip()
    chars_in = len(message)
    if chars_in > self.INPUT_LIMIT:
      self.input_window.delete("%s-%dc" % (tk.INSERT, 
        chars_in - self.INPUT_LIMIT), tk.INSERT)
    # Boilerplate for the <<Modified>> virtual event
    self.input_window.tk.call(self.input_window._w, 'edit', 'modified', 0)

    

  def createWidgets(self):
    self.output_window = tk.Text(self, height=30)
    self.output_window.config(state=tk.DISABLED)
    self.output_window.grid()
    
    initial_input_text = "Enter Text Here"
    self.input_window_chars = len(initial_input_text)
    self.input_window = tk.Text(self, height=5)
    self.input_window.insert(tk.END, initial_input_text)
    self.input_window.bind("<Return>", self.messageSendEventHandler)
    # Boilerplate for the <<Modified>> virtual event
    self.input_window.tk.call(self.input_window._w, 'edit', 'modified', 0)
    self.input_window.bind("<<Modified>>", self.messageLimitSizeHandler)
    self.input_window.grid()

    self.users_window = tk.Text(self, height=5)
    self.users_window.config(state=tk.DISABLED)
    self.users_window.grid()


# Main method
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Username required as a command line parameter."
    sys.exit()
  name = sys.argv[1]
  controller = ChatClientController(name)

  app = TKChatClient(controller)
  controller.view = app
  app.master.title('%s\'s Chat Room' % name)
  app.after(500, app.refresh)
  app.mainloop()
