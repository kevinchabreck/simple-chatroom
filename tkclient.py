#!/usr/bin/env python

import Tkinter as tk

class TKChatClient(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    self.output_window = tk.Text(self)
    self.output_window.insert(tk.END, "output window")
    self.output_window.grid()
    
    self.input_window = tk.Text(self)
    self.input_window.insert(tk.END, "input window")
    self.input_window.grid()

    self.users_window = tk.Text(self)
    self.users_window.insert(tk.END, "users window")
    self.users_window.grid()



# Main method
if __name__ == "__main__":
  app = TKChatClient()
  app.master.title('<user>\'s Chat Room')
  app.mainloop()
