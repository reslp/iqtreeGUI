#! /usr/bin/env python
# tkinter window for settings
# written by Philipp Resl
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

#import ttk
#import tkFileDialog, tkMessageBox

class AlignmentView():
	def __init__(self, master, alignment, filename):
		self.master = master
		self.master.title(alignment)
		self.master.grid_columnconfigure(0,weight=1)
		self.master.grid_rowconfigure(0,weight=1)
		#self.master.geometry("500x400")		
		self.alignment_text = ScrolledText(self.master)
		self.alignment_text.grid(row=0,column=0,sticky=tk.N+tk.S+tk.W+tk.E)
		file = open(filename, "U")
		sequence = ""
		for line in file.readlines():
			sequence += line
		file.close()
		self.alignment_text.insert(tk.END, sequence)
		
		