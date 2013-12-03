#!/usr/bin/env python

import Tkinter as tk
import sys
from chat_client_controller import *

class TKChatClient(tk.Frame):
  INPUT_LIMIT = 100

  def __init__(self, controller, master=None):
    tk.Frame.__init__(self, master)
    self.controller = controller
    self.grid()
    self.createWidgets()

  def refresh(self):
    print "Refreshing"
    self.controller.updateOutput()
    self.controller.updateUsers()
    self.controller.updateCanvas()
    self.after(1000, self.refresh)


  def updateUsers(self, users_list):
    self.users_window.config(state=tk.NORMAL)
    self.users_window.delete(1.0, tk.END)
    self.users_window.insert(tk.END, ", ".join(users_list))
    self.users_window.config(state=tk.DISABLED)


  def appendMessage(self, message):
    self.output_window.config(state=tk.NORMAL)
    self.output_window.insert(tk.END, message + "\n")
    self.output_window.config(state=tk.DISABLED)

  def appendCanvasMessage(self, message_tuple):
    center_x = int(message_tuple[0])
    center_y = int(message_tuple[1])
    radius = int(message_tuple[2])
    color = message_tuple[3]

    # Tkinter's bounding box is the xy of the top left and bottom right
    bbox = (center_x - radius, center_y - radius, 
        center_x + radius, center_y + radius)
    self.canvas.create_oval(bbox, fill = color, outline="")    



  def sendMessage(self, event):
    message = self.input_window.get(1.0, tk.END).strip()
    print "Sending message: '%s'" % message
    self.input_window.delete(1.0, tk.END)
    self.input_window_chars = 0
    self.controller.sendMessage(message)

  def limitInputSize(self, event):
    print "Testing limiting"
    message = self.input_window.get(1.0, tk.END).strip()
    chars_in = len(message)
    if chars_in > self.INPUT_LIMIT:
      self.input_window.delete("%s-%dc" % (tk.INSERT, 
        chars_in - self.INPUT_LIMIT), tk.INSERT)
    # Boilerplate for the <<Modified>> virtual event
    self.input_window.tk.call(self.input_window._w, 'edit', 'modified', 0)


  def paintHandler(self, event):
    center_x = event.x
    center_y = event.y
    radius = 10
    color = "#00FF00"

    self.controller.sendCanvasMessage(center_x, center_y, radius, color)

  def createWidgets(self):
    self.output_window = tk.Text(self, height=30)
    self.output_window.config(state=tk.DISABLED)
    self.output_window.grid()
    
    initial_input_text = "Enter Text Here"
    self.input_window_chars = len(initial_input_text)
    self.input_window = tk.Text(self, height=5)
    self.input_window.insert(tk.END, initial_input_text)
    self.input_window.bind("<Return>", self.sendMessage)
    # Boilerplate for the <<Modified>> virtual event
    self.input_window.tk.call(self.input_window._w, 'edit', 'modified', 0)
    self.input_window.bind("<<Modified>>", self.limitInputSize)
    self.input_window.grid()

    self.users_window = tk.Text(self, height=5)
    self.users_window.config(state=tk.DISABLED)
    self.users_window.grid()

    self.canvas = tk.Canvas(self, width=500, height=500, bg="#ffffff")
    self.canvas.bind("<1>", self.paintHandler)
    self.canvas.grid(column=1, row=0, rowspan=3)


# Main method
if __name__ == "__main__":
  name = sys.argv[1]
  controller = ChatClientController(name)
  app = TKChatClient(controller)
  controller.view = app
  app.master.title('%s\'s Chat Room' % name)
  app.after(500, app.refresh)
  app.mainloop()

# TODO: Handle when the server closes.
