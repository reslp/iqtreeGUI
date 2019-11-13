#! /usr/bin/env python
# add credits...
import sys
from tkinter import *
from tkinter.ttk import *

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
		yscrollbar = Scrollbar(parent)#, width=15)
		yscrollbar.pack(side=RIGHT, fill=Y, expand=False)

		# canvas on left in parent
		#plain_can_style = Style()
		#plain_can_style.configure("plain_canvas.TCanvas", foreground="green", background="red")
		self.canvas = Canvas(parent, yscrollcommand=yscrollbar.set, bd=0, highlightthickness=0, relief='ridge', background="#ECECEC")
		#self.canvas.config(bg="gray85")
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

		def fill_canvas(event):
			"enlarge the windows item to the canvas width"
			canvas_width = event.width
			self.canvas.itemconfig(self.windows_item, width = canvas_width)

		self.canvas.bind('<Configure>', fill_canvas)

		yscrollbar.config(command=self.canvas.yview)    
		
		#plain_style = Style()
		#plain_style.configure("plain_st.TFrame", foreground="black", background="#F0F0F0")
		
		#self.configure(style="plain_style")
		
		# create the scrollable frame and assign it to the windows item of the canvas
		Frame.__init__(self, parent, *args, **kw)
		self.windows_item = self.canvas.create_window(-1,-1, window=self, anchor=NW)

	def update(self):
		"""
		Update changes to the canvas before the program gets
		back the mainloop, then update the scrollregion
		"""
		self.update_idletasks()
		self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
