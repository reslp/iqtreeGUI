#! /usr/bin/env python
# tkinter window for computing Robinson-Foulds distances
# written by Philipp Resl
import os
import Tkinter as tk
import ttk
import tkFileDialog, tkMessageBox
from iqtree_out import *


class RobinsonFouldsWindow():
	treeset1 = ""
	treeset2 = ""
	
	def load_tree1(self):
		self.treeset1 = tkFileDialog.askopenfilename(initialdir = "~",title = "Select multi tree file")
		if self.treeset1 == "":
			self.tree_file_label.configure(text="no treefile loaded")
		else:
			self.tree1_file_label.configure(text=self.treeset1)
	
	def load_tree2(self):
		self.treeset2 = tkFileDialog.askopenfilename(initialdir = "~",title = "Select a target tree file")
		if self.treeset2 == "":
			self.tree2_file_label.configure(text="no target tree specified")
		else:
			self.tree2_file_label.configure(text=self.treeset2)
	
	def spawn_iqtree_subprocess(self, command, settings):	
		iqtree_out_window=Toplevel(self.master)
		iqtree_out = IqtreeWindow(iqtree_out_window, self.settings)
		iqtree_out.send_command(command)
		iqtree_out.spawn_process()
	
	def __init__(self, master, settings):
		self.settings = settings
		self.master = master
		self.master.title("Robinson-Foulds distances")
		self.settings_frame = tk.Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = tk.Label(self.settings_frame,text="Calculate Robinson-Foulds distance", justify=tk.LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=20)
		

		self.tree1_label = tk.Label(self.settings_frame, text="Specify first multi-tree file (-t):", justify=tk.LEFT)
		self.tree1_label.grid(row=3,column=1, sticky=tk.W, columnspan=2)
		
		self.tree1_button = tk.Button(self.settings_frame, text="Load", justify=tk.LEFT, command=self.load_tree1)
		self.tree1_button.grid(row=3,column=3, sticky=tk.W)
		
		self.tree1_file_label = tk.Label(self.settings_frame, text="no treefile loaded", justify=tk.LEFT, wraplength=500)
		self.tree1_file_label.configure(foreground="grey")
		self.tree1_file_label.grid(row=4,column=1, sticky=tk.W)
		
		self.tree2_label = tk.Label(self.settings_frame, text="Specify second multi-tree file (-rf):", justify=tk.LEFT)
		self.tree2_label.grid(row=5,column=1, sticky=tk.W, columnspan=2)
		
		self.tree2_button = tk.Button(self.settings_frame, text="Load", justify=tk.LEFT, command=self.load_tree2)
		self.tree2_button.grid(row=5,column=3, sticky=tk.W)
		
		self.tree2_file_label = tk.Label(self.settings_frame, text="no treefile loaded", justify=tk.LEFT, wraplength=500)
		self.tree2_file_label.configure(foreground="grey")
		self.tree2_file_label.grid(row=6,column=1, sticky=tk.W)
		
		self.rf_all_var = tk.IntVar()
		self.rf_all_var.set(1)
		self.rf_adj_var = tk.IntVar()
		self.rf_adj_var.set(0)
		
		def rf_all_m():
			self.rf_all_var.set(1)
			self.rf_adj_var.set(0)
		def rf_adj_m():
			self.rf_all_var.set(0)
			self.rf_adj_var.set(1)
					
		self.all = tk.Checkbutton(self.settings_frame, text="Compute all-to-all RF distances between all trees in first tree set (-rf_all)", variable=self.rf_all_var, command=rf_all_m)
		self.all.grid(row=7,column=1, sticky=tk.W)
		self.adj = tk.Checkbutton(self.settings_frame, text="Compute RF distances between adjacent trees in first tree set (-rf_adj)", variable=self.rf_adj_var, command=rf_adj_m)
		self.adj.grid(row=8,column=1, sticky=tk.W)
		
		self.settings_frame.rowconfigure(18, minsize=20)
		
		def calc():
			print self.settings
			cmd = self.settings.iqtree_path
			if self.treeset1 != "" and self.treeset2 != "":
				cmd += " -rf %s" % self.treeset1
				cmd += " %s" % self.treeset2
			elif self.treeset1 != "" and self.treeset2 == "":
				if self.rf_all_var.get() == 1:
					cmd += " -rf_all %s" % self.treeset1
				if self.rf_adj_var.get() == 1:
					cmd += " -rf_adj %s" % self.treeset1
			else:
				tkMessageBox.showinfo("No input trees", "You need to specify at least one tree file.")
				return
			print cmd
			self.spawn_iqtree_subprocess(cmd, self.settings)

				
		
		
		self.apply_button = tk.Button(self.settings_frame, text="Calculate Robinson-Foulds distance", command=calc)
		self.apply_button.grid(row=19, column=12, sticky=tk.W)
		self.cancel_button = tk.Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=tk.W)
		
		self.settings_frame.grid()
		