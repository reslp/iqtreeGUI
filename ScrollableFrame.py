#! /usr/bin/env python
# add credits...
import sys

try:
    from tkinter import *
except ImportError:
    from tkinter import *

try:
    import tkinter.ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

class ScrollableFrame(Frame):
	"""
	Consider me a regular frame with a vertical scrollbar 
	on the right, after adding/removing widgets to/from me 
	call my method update() to refresh the scrollable area. 
	Don't pack() me, nor place() nor grid(). 
	I work best when I am alone in the parent frame.
	"""
	def __init__(self, parent, *args, **kw):

		# scrollbar on right in parent 
		yscrollbar = Scrollbar(parent, width=32)
		yscrollbar.pack(side=RIGHT, fill=Y, expand=False)

		# canvas on left in parent
		self.canvas = Canvas(parent, yscrollcommand=yscrollbar.set)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

		def fill_canvas(event):
			"enlarge the windows item to the canvas width"
			canvas_width = event.width
			self.canvas.itemconfig(self.windows_item, width = canvas_width)

		self.canvas.bind('<Configure>', fill_canvas)

		yscrollbar.config(command=self.canvas.yview)    

		# create the scrollable frame and assign it to the windows item of the canvas
		Frame.__init__(self, parent, *args, **kw)
		self.windows_item = self.canvas.create_window(0,0, window=self, anchor=NW)

	def update(self):
		"""
		Update changes to the canvas before the program gets
		back the mainloop, then update the scrollregion
		"""
		self.update_idletasks()
		self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
