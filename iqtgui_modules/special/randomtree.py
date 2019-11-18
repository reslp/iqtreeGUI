#! /usr/bin/env python
# tkinter window for computing Robinson-Foulds distances
# written by Philipp Resl
import os
from tkinter import *
import tkinter.filedialog, tkinter.messagebox
from tkinter.ttk import *
#from iqtree_out import *
from iqtgui_modules import iqtree_out as iqto

class RandomTreeWindow():
	def spawn_iqtree_subprocess(self, command, settings):	
		iqtree_out_window=Toplevel(self.master)
		iqtree_out = iqto.IqtreeWindow(iqtree_out_window, self.settings)
		iqtree_out.send_command(command)
		iqtree_out.spawn_process()
		
	def __init__(self, master, settings):
		self.settings = settings
		self.master = master
		self.master.title("Create random trees")
		self.settings_frame = Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = Label(self.settings_frame,text="Generate random trees", justify=LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=20)
		
		self.ntips = Label(self.settings_frame, text="Specify the number of taxa in the random tree", justify=LEFT, wraplength=500)
		self.ntips.grid(row=3,column=1, sticky=W, columnspan=5)
		
		self.r_entry = Entry(self.settings_frame, width=5)
		self.r_entry.insert(END, 100)
		self.r_entry.grid(row=3,column=2, sticky=W+N)
		
		self.r_var = IntVar()
		self.r_var.set(1)
		self.ru_var = IntVar()
		self.ru_var.set(0)
		self.rcat_var = IntVar()
		self.rcat_var.set(0)
		self.rbal_var = IntVar()
		self.rbal_var.set(0)
		self.rcsg_var = IntVar()
		self.rcsg_var.set(0)
		
		def r_m():
			self.r_var.set(1)
			self.ru_var.set(0)
			self.rcat_var.set(0)
			self.rbal_var.set(0)
			self.rcsg_var.set(0)
		def ru_m():
			self.r_var.set(0)
			self.ru_var.set(1)
			self.rcat_var.set(0)
			self.rbal_var.set(0)
			self.rcsg_var.set(0)
		def rcat_m():
			self.r_var.set(0)
			self.ru_var.set(0)
			self.rcat_var.set(1)
			self.rbal_var.set(0)
			self.rcsg_var.set(0)
		def rbal_m():
			self.r_var.set(0)
			self.ru_var.set(0)
			self.rcat_var.set(0)
			self.rbal_var.set(1)
			self.rcsg_var.set(0)	
		def rcsg_m():
			self.r_var.set(0)
			self.ru_var.set(0)
			self.rcat_var.set(0)
			self.rbal_var.set(0)
			self.rcsg_var.set(1)
		
		self.r = Checkbutton(self.settings_frame, text="Generate random tree under Yule-Harding Model (-r)", variable=self.r_var, command=r_m)
		self.r.grid(row=4,column=1, sticky=W)
		self.ru = Checkbutton(self.settings_frame, text="Generate random tree under uniform model (-ru)", variable=self.ru_var, command=ru_m)
		self.ru.grid(row=5,column=1, sticky=W)
		self.rcat = Checkbutton(self.settings_frame, text="Generate a random catapillar tree (-rcat)", variable=self.rcat_var, command=rcat_m)
		self.rcat.grid(row=6,column=1, sticky=W)
		self.rbal = Checkbutton(self.settings_frame, text="Generate random balanced tree (-rbal)", variable=self.rbal_var, command=rbal_m)
		self.rbal.grid(row=7,column=1, sticky=W)
		self.rcsg = Checkbutton(self.settings_frame, text="Generate random circular split network (-rcsg)", variable=self.rcsg_var, command=rcsg_m)
		self.rcsg.grid(row=7,column=1, sticky=W)
		
		self.br = Label(self.settings_frame, text="Specify branch-lengths of random tree:", justify=LEFT, wraplength=500)
		self.br.grid(row=8,column=1, sticky=W, columnspan=5)
		
		self.min = Label(self.settings_frame, text="Minimum:", justify=LEFT, wraplength=500)
		self.min.grid(row=9,column=1, sticky=W, columnspan=2)
		self.min_entry = Entry(self.settings_frame, width=5)
		self.min_entry.insert(END, 0.001)
		self.min_entry.grid(row=9,column=3, sticky=W+N)
		
		self.mean = Label(self.settings_frame, text="Mean:", justify=LEFT, wraplength=500)
		self.mean.grid(row=10,column=1, sticky=W, columnspan=2)
		self.mean_entry = Entry(self.settings_frame, width=5)
		self.mean_entry.insert(END, 0.1)
		self.mean_entry.grid(row=10,column=3, sticky=W+N)
		
		self.max = Label(self.settings_frame, text="Max:", justify=LEFT, wraplength=500)
		self.max.grid(row=11,column=1, sticky=W, columnspan=2)
		self.max_entry = Entry(self.settings_frame, width=5)
		self.max_entry.insert(END, 0.999)
		self.max_entry.grid(row=11,column=3, sticky=W+N)
		
		self.not_yet = Label(self.settings_frame,text="Functionality currently not implemented:\nNaming trees according to names from alignment (-s)", justify=LEFT)
		self.not_yet.configure(foreground="red")
		self.not_yet.grid(row=17,column=1, sticky=W, columnspan=5)
		
		self.filename = Label(self.settings_frame, text="Filename:", justify=LEFT, wraplength=500)
		self.filename.grid(row=18,column=1, sticky=W, columnspan=2)
		self.filename_entry = Entry(self.settings_frame, width=20)
		self.filename_entry.insert(END, "random_trees.tre")
		self.filename_entry.grid(row=18,column=3, sticky=W+N)
		
		self.settings_frame.rowconfigure(19, minsize=20)
		
		def create_random():
			try:
				ntrees = int(self.r_entry.get())
			except ValueError:
				tkinter.messagebox.showinfo("Wrong value", "Specified number of taxa is incorrect")
				return	
			print(self.settings.iqtree_path)
			cmd = self.settings.iqtree_path
			if self.r_var.get() == 1:
				cmd += " -r %d" % ntrees
			if self.ru_var.get() ==1:
				cmd += " -ru %d" % ntrees
			if self.rcat_var.get() == 1:
				cmd += " -rcat %d" % ntrees
			if self.rcsg_var.get() == 1:
				cmd += " -rcsg %d" % ntrees
			try:
				min = float(self.min_entry.get())
				mean = float(self.mean_entry.get())
				max = float(self.max_entry.get())
				cmd += " -rlen %f" % min
				cmd += " %f" % mean
				cmd += " %f" % max	
			except ValueError:
				tkinter.messagebox.showinfo("Wrong value", "One of the entered values (min, mean, max) is incorrect")
				return
			if self.filename_entry.get() == "":
				cmd +=  " random_trees.tre -redo"
			else:
				cmd +=  " %s -redo" % self.filename_entry.get()
			
			print(cmd)
			self.spawn_iqtree_subprocess(cmd, self.settings)
		
		self.apply_button = Button(self.settings_frame, text="Generate random tree", command=create_random)
		self.apply_button.grid(row=20, column=12, sticky=W)
		self.cancel_button = Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=20, column=11, sticky=W)
		

		
		self.settings_frame.grid()