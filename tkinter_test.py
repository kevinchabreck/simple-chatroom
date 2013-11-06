#!/usr/bin/env python

# Sample tk code from
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/minimal-app.html

import Tkinter as tk

class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    self.quitButton = tk.Button(self, text='Quit',
        command = self.quit)
    self.quitButton.grid()

app = Application()
app.master.title('Sample application')
app.mainloop()
