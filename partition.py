#! /usr/bin/env python
# tkinter Frame for partition selection
# written by Philipp Resl
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

class Partition(Frame):
	partition_id = ""

	
	def get_start(self): #returning beginning of partition
		return self.start_entry.get() 
	
	def get_end(self): #returning end of partition
		return self.end_entry.get()

	def get_which_alignment(self): #returning the alignment number of partition
		return int(self.which_alignment.split(" ")[1])
		
		
	def create_widgets(self):
		self.partition_label = Label(self, text=self.partition_id)
		#self.partition_label.place(relx=0, rely=0, width=200, height=50)
		self.partition_label.grid(row=0,column=0)
		self.partition_label.configure(font=("TkTextFont", 12, "bold"))
		self.partition_start_label = Label(self, text="Start: ")
		self.partition_start_label.grid(row=0,column=2)
		self.start_entry = Entry(self, width=6)
		self.start_entry.grid(row=0,column=3)
		self.partition_end_label = Label(self, text="End: ")
		self.partition_end_label.grid(row=0,column=4)
		self.end_entry = Entry(self, width=6)
		self.end_entry.grid(row=0,column=5)
		
		print(self.alignments)
		self.part_alignment_var = StringVar()
		self.part_alignment_var.set(self.alignments[0])
		
		def alignOption(which):
			self.which_alignment = which
			print(which)
			
		self.which_partition_model = OptionMenu(self, self.part_alignment_var,  *self.alignments, command=alignOption)
		self.which_partition_model.grid(row=0,column=6, sticky=N)
		
	def __init__(self, master, part_id, alignments, number):
		Frame.__init__(self, master)
		self.master = master
		self.alignments = alignments
		self.partition_id = part_id
		self.partition_no = number
		self.which_alignment = "Alignment 1"
		self.create_widgets()