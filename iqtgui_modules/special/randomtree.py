#! /usr/bin/env python
# tkinter window for computing Robinson-Foulds distances
# written by Philipp Resl
import os
import tkinter as tk
import tkinter.ttk
import tkinter.filedialog, tkinter.messagebox
#from iqtree_out import *
from iqtgui_modules import iqtree_out

class RandomTreeWindow():
	def spawn_iqtree_subprocess(self, command, settings):	
		iqtree_out_window=Toplevel(self.master)
		iqtree_out = IqtreeWindow(iqtree_out_window, self.settings)
		iqtree_out.send_command(command)
		iqtree_out.spawn_process()
		
	def __init__(self, master, settings):
		self.settings = settings
		self.master = master
		self.master.title("Create random trees")
		self.settings_frame = tk.Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = tk.Label(self.settings_frame,text="Generate random trees", justify=tk.LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=20)
		
		self.ntips = tk.Label(self.settings_frame, text="Specify the number of taxa in the random tree", justify=tk.LEFT, wraplength=500)
		self.ntips.grid(row=3,column=1, sticky=tk.W, columnspan=5)
		
		self.r_entry = tk.Entry(self.settings_frame, width=5)
		self.r_entry.insert(tk.END, 100)
		self.r_entry.grid(row=3,column=6, sticky=tk.W+tk.N)
		
		self.r_var = tk.IntVar()
		self.r_var.set(1)
		self.ru_var = tk.IntVar()
		self.ru_var.set(0)
		self.rcat_var = tk.IntVar()
		self.rcat_var.set(0)
		self.rbal_var = tk.IntVar()
		self.rbal_var.set(0)
		self.rcsg_var = tk.IntVar()
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
		
		self.r = tk.Checkbutton(self.settings_frame, text="Generate random tree under Yule-Harding Model (-r)", variable=self.r_var, command=r_m)
		self.r.grid(row=4,column=1, sticky=tk.W)
		self.ru = tk.Checkbutton(self.settings_frame, text="Generate random tree under uniform model (-ru)", variable=self.ru_var, command=ru_m)
		self.ru.grid(row=5,column=1, sticky=tk.W)
		self.rcat = tk.Checkbutton(self.settings_frame, text="Generate a random catapillar tree (-rcat)", variable=self.rcat_var, command=rcat_m)
		self.rcat.grid(row=6,column=1, sticky=tk.W)
		self.rbal = tk.Checkbutton(self.settings_frame, text="Generate random balanced tree (-rbal)", variable=self.rbal_var, command=rbal_m)
		self.rbal.grid(row=7,column=1, sticky=tk.W)
		self.rcsg = tk.Checkbutton(self.settings_frame, text="Generate random circular split network (-rcsg)", variable=self.rcsg_var, command=rcsg_m)
		self.rcsg.grid(row=7,column=1, sticky=tk.W)
		
		self.br = tk.Label(self.settings_frame, text="Specify branch-lengths of random tree:", justify=tk.LEFT, wraplength=500)
		self.br.grid(row=8,column=1, sticky=tk.W, columnspan=5)
		
		self.min = tk.Label(self.settings_frame, text="Minimum:", justify=tk.LEFT, wraplength=500)
		self.min.grid(row=9,column=1, sticky=tk.W, columnspan=2)
		self.min_entry = tk.Entry(self.settings_frame, width=5)
		self.min_entry.insert(tk.END, 0.001)
		self.min_entry.grid(row=9,column=3, sticky=tk.W+tk.N)
		
		self.mean = tk.Label(self.settings_frame, text="Mean:", justify=tk.LEFT, wraplength=500)
		self.mean.grid(row=10,column=1, sticky=tk.W, columnspan=2)
		self.mean_entry = tk.Entry(self.settings_frame, width=5)
		self.mean_entry.insert(tk.END, 0.1)
		self.mean_entry.grid(row=10,column=3, sticky=tk.W+tk.N)
		
		self.max = tk.Label(self.settings_frame, text="Max:", justify=tk.LEFT, wraplength=500)
		self.max.grid(row=11,column=1, sticky=tk.W, columnspan=2)
		self.max_entry = tk.Entry(self.settings_frame, width=5)
		self.max_entry.insert(tk.END, 0.999)
		self.max_entry.grid(row=11,column=3, sticky=tk.W+tk.N)
		
		self.not_yet = tk.Label(self.settings_frame,text="Functionality currently not implemented:\nNaming trees according to names from alignment (-s)", justify=tk.LEFT)
		self.not_yet.configure(foreground="red")
		self.not_yet.grid(row=17,column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(18, minsize=20)
		
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
			cmd += " random_trees.trees -redo"
			print(cmd)
			self.spawn_iqtree_subprocess(cmd, self.settings)
		
		self.apply_button = tk.Button(self.settings_frame, text="Generate random tree", command=create_random)
		self.apply_button.grid(row=19, column=12, sticky=tk.W)
		self.cancel_button = tk.Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=tk.W)
		

		
		self.settings_frame.grid()