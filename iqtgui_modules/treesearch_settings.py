#! /usr/bin/env python
# tkinter window for treesearch settings
# written by Philipp Resl
import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog, tkinter.messagebox

class TreesearchSettingsWindow():
	filename = ""
	
	def load_tree(self):
		self.filename = tkinter.filedialog.askopenfilename(initialdir = "~",title = "Select starting tree")
		self.start_tree_path.grid(row=3,column=2, sticky=W)
		self.start_tree_path.configure(text=self.filename)
		
	def __init__(self, master, data):
		self.master = master
		self.master.title("Treesearch settings")
		self.settings_frame = Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = Label(self.settings_frame,text="Advanced settings of the tree search functionality", justify=LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=30)
		
		self.allnni_var = IntVar()
		self.allnni_var.set(data.allnni)
		self.allnni = Checkbutton(self.settings_frame, text="Use thorough (but slower) NNI search (-allnni)", variable=self.allnni_var)
		self.allnni.grid(row=3,column=1, sticky=W, columnspan=5)
		
		self.djc_var = IntVar()
		self.djc_var.set(data.djc)
		self.djc = Checkbutton(self.settings_frame, text="Avoid computing ML pairwise distances and BIONJ tree (-djc)", variable=self.djc_var)
		self.djc.grid(row=4,column=1, sticky=W, columnspan=5)
		
		self.fast_var = IntVar()
		self.fast_var.set(data.fast)
		self.fast = Checkbutton(self.settings_frame, text="Use fast tree search mode (-fast)", variable=self.fast_var)
		self.fast.grid(row=5,column=1, sticky=W, columnspan=5)
		
		self.ninit_label = Label(self.settings_frame, text="Number of initial parsimony trees (-ninit): ", justify=LEFT)
		self.ninit_label.grid(row=7, column=1, sticky=W+N)
		self.ninit_entry = Entry(self.settings_frame)
		self.ninit_entry.insert(END, data.ninit)
		self.ninit_entry.grid(row=7,column=2, sticky=W+N)
		
		self.n_label = Label(self.settings_frame, text="Number of iterations to stop (-n): ", justify=LEFT)
		self.n_label.grid(row=8, column=1, sticky=W+N)
		self.n_entry = Entry(self.settings_frame)
		self.n_entry.insert(END, data.n)
		self.n_entry.grid(row=8,column=2, sticky=W+N)
		
		self.ntop_label = Label(self.settings_frame, text="Number of top initial parsimony trees (-ntop): ", justify=LEFT)
		self.ntop_label.grid(row=9, column=1, sticky=W+N)
		self.ntop_entry = Entry(self.settings_frame)
		self.ntop_entry.insert(END, data.ntop)
		self.ntop_entry.grid(row=9,column=2, sticky=W+N)
		
		self.nbest_label = Label(self.settings_frame, text="Number of trees in candidate set for ML search (-nbest): ", justify=LEFT)
		self.nbest_label.grid(row=10, column=1, sticky=W+N)
		self.nbest_entry = Entry(self.settings_frame)
		self.nbest_entry.insert(END, data.nbest)
		self.nbest_entry.grid(row=10,column=2, sticky=W+N)
		
		self.nstop_label = Label(self.settings_frame, text="Number of unsuccessful iterations to stop (-nstop): ", justify=LEFT)
		self.nstop_label.grid(row=11, column=1, sticky=W+N)
		self.nstop_entry = Entry(self.settings_frame)
		self.nstop_entry.insert(END, data.nstop)
		self.nstop_entry.grid(row=11,column=2, sticky=W+N)
		
		self.pers_label = Label(self.settings_frame, text="Pertubation strength (-pers): ", justify=LEFT)
		self.pers_label.grid(row=12, column=1, sticky=W+N)
		self.pers_entry = Entry(self.settings_frame)
		self.pers_entry.insert(END, data.pers)
		self.pers_entry.grid(row=12,column=2, sticky=W+N)
		
		self.sprrad_label = Label(self.settings_frame, text="SPR radius for initial parsimony tree search (-sprrad): ", justify=LEFT)
		self.sprrad_label.grid(row=13, column=1, sticky=W+N)
		self.sprrad_entry = Entry(self.settings_frame)
		self.sprrad_entry.insert(END, data.sprrad)
		self.sprrad_entry.grid(row=13,column=2, sticky=W+N)
		
		
		def apply():
			try:
				data.allnni = self.allnni_var.get()
				data.djc = self.djc_var.get()
				data.fast = self.fast_var.get()
				data.ninit = int(self.ninit_entry.get())
				data.n = int(self.n_entry.get())
				data.ntop = int(self.ntop_entry.get())
				data.nbest = int(self.nbest_entry.get())
				data.nstop = int(self.nstop_entry.get())
				data.pers = float(self.pers_entry.get())
				data.sprrad = int(self.sprrad_entry.get())
				self.master.destroy()	
			except ValueError:
				tkinter.messagebox.showinfo("Error", "Some of the entered values are incorrect")
		
		self.apply_button = Button(self.settings_frame, text="Apply & Close", command=apply)
		self.apply_button.grid(row=19, column=12, sticky=W)
		self.cancel_button = Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=W)
		
		self.settings_frame.grid()