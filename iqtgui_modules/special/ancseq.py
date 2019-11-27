#! /usr/bin/env python
# tkinter window for computing Robinson-Foulds distances
# written by Philipp Resl
import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog, tkinter.messagebox
#from iqtree_out import *
from iqtgui_modules import iqtree_out as iqtout

class AncSeqWindow():
	tree = ""
	ppcutoff = 0.95
	
	def load_tree1(self):
		self.tree = tkinter.filedialog.askopenfilename(initialdir = "~",title = "Select tree file")
		if self.tree == "":
			self.tree_file_label.configure(text="no treefile loaded, will infer the tree during ancestral state reconstruction")
		else:
			self.tree_file_label.configure(text=self.tree)

	def spawn_iqtree_subprocess(self, command, settings):	
		iqtree_out_window=Toplevel(self.master)
		iqtree_out = iqtout.IqtreeWindow(iqtree_out_window, self.settings)
		iqtree_out.send_command(command)
		iqtree_out.spawn_process()

	def return_state(self):
		return self.set_var.get()
	
	def __init__(self, master, settings, anc_settings):
		self.anc_settings = anc_settings
		self.settings = settings
		self.master = master
		self.master.title("Ancestral sequence reconstruction")
		self.settings_frame = Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = Label(self.settings_frame,text="Reconstruct ancestral states")
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W, columnspan=5)
		self.description2 = Label(self.settings_frame,text="Select options for ancestral sequence reconstruction. Click save afterwards and then run analysis.")
		self.description2.grid(row=2,column=1, sticky=W, columnspan=5)
		
		self.settings_frame.rowconfigure(3, minsize=20)
		
		self.set_var = IntVar()
		self.set_var.set(0)
		
		def set_m():
			print(self.set_var.get())
					
		self.set = Checkbutton(self.settings_frame, text="Perform ancestral sequence reconstruction", variable=self.set_var, command=set_m)
		self.set.grid(row=4,column=1, sticky=W)
			
		self.tree1_label = Label(self.settings_frame, text="Optionally, specify a tree (-te):")
		self.tree1_label.grid(row=5,column=1, sticky=W, columnspan=2)
		
		self.tree1_button = Button(self.settings_frame, text="Load", command=self.load_tree1)
		self.tree1_button.grid(row=5,column=3, sticky=W)
		
		self.tree_file_label = Label(self.settings_frame, text="no treefile loaded, will infer the tree during ancestral state reconstruction", wraplength=500)
		self.tree_file_label.configure(foreground="grey")
		self.tree_file_label.grid(row=6,column=1, sticky=W)
		
		self.ppcut = Label(self.settings_frame, text="Specify posterior probability cutoff (-asr-min):", justify=LEFT, wraplength=500)
		self.ppcut.grid(row=7,column=1, sticky=W, columnspan=2)
		
		self.ppcut_entry = Entry(self.settings_frame, width=5)
		self.ppcut_entry.insert(END, self.ppcutoff)
		self.ppcut_entry.grid(row=7,column=3, sticky=W+N)
			
		self.anc_var = IntVar()
		self.anc_var.set(0)
		
		def anc_m():
			print(self.anc_var.get())
				
		self.anc = Checkbutton(self.settings_frame, text="Write the ancestral states to a .states file (-anc)", variable=self.anc_var, command=anc_m)
		self.anc.grid(row=8,column=1, sticky=W)
			
		self.settings_frame.rowconfigure(18, minsize=20)
		
		def save_settings():
			self.anc_settings.set = self.set_var.get()
			
			if self.tree != "":
				self.anc_settings.tree += "-te %s " % self.tree
			
			if self.anc_var.get() == 1:
				self.anc_settings.anc = "-asr "
			
			self.anc_settings.ppcut = "-asr-min %s " % self.ppcut_entry.get()
			
			self.master.destroy()
			#self.spawn_iqtree_subprocess(cmd, self.settings)

		self.apply_button = Button(self.settings_frame, text="Save", command=save_settings)
		self.apply_button.grid(row=19, column=12, sticky=W)
		self.cancel_button = Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=W)
		
		self.settings_frame.grid()
		