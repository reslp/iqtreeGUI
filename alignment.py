#! /usr/bin/env python
# tkinter Frame for importing multiple alignments
# written by Philipp Resl
from alignment_view import *

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

class Alignment(Frame):
	alignment_id = ""
	alignment_path = ""
	
	def show_alignment(self):
		window = Toplevel()
		al_window = AlignmentView(window, alignment=self.alignment_id, filename=self.alignment_path)
		self.master.wait_window(al_window)
		

	def create_widgets(self):
		self.alignment_label = Label(self, text=self.alignment_id)
		self.alignment_label.grid(row=0,column=3)
		self.alignment_label.configure(font=("TkTextFont", 12, "bold"))
		self.alignment_path_label = Label(self, text=self.alignment_path)
		self.alignment_path_label.grid(row=0,column=4)
		self.view_button = Button(self, text="View", command=self.show_alignment)
		self.view_button.grid(row=0,column=1)
		#self.remove_button = Button(self, text="Remove")
		#self.remove_button.grid(row=0,column=2)
		
	def __init__(self, master, align_id, path, number):
		Frame.__init__(self, master)
		self.master = master
		self.alignment_id = align_id
		self.alignment_path = path
		self.alignment_no = number
		self.create_widgets()