#! /usr/bin/env python
# tkinter window for creating consensus trees
# written by Philipp Resl
import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog, tkinter.messagebox
#from iqtree_out import *
from iqtgui_modules import iqtree_out as iqtout

class ConsensusTreeWindow():
	filename = ""
	target_filename = ""
	
	def load_tree(self):
		self.filename = tkinter.filedialog.askopenfilename(initialdir = "~",title = "Select multi tree file")
		if self.filename == "":
			self.tree_file_label.configure(text="no treefile loaded")
		else:
			self.tree_file_label.configure(text=self.filename)
	
	def load_target_tree(self):
		self.target_filename = tkinter.filedialog.askopenfilename(initialdir = "~",title = "Select a target tree file")
		if self.filename == "":
			self.sup_label.configure(text="no target tree specified")
		else:
			self.sup_label.configure(text=self.target_filename)
	
	def spawn_iqtree_subprocess(self, command, settings):	
		iqtree_out_window=Toplevel(self.master)
		iqtree_out = iqtout.IqtreeWindow(iqtree_out_window, self.settings)
		iqtree_out.send_command(command)
		iqtree_out.spawn_process()
	
	def __init__(self, master, settings):
		self.settings = settings
		self.master = master
		self.master.title("Create Consensus trees")
		self.settings_frame = Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
	
		self.description = Label(self.settings_frame,text="Constructing consensus tree")
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=20)
		self.tree_label = Label(self.settings_frame, text="Specify multi-tree file (-t):")
		self.tree_label.grid(row=3,column=1, sticky=W, columnspan=2)
		
		self.tree_button = Button(self.settings_frame, text="Load", command=self.load_tree)
		self.tree_button.grid(row=3,column=2, sticky=W)
		
		self.tree_file_label = Label(self.settings_frame, text="no treefile loaded", wraplength=500)
		self.tree_file_label.configure(foreground="grey")
		self.tree_file_label.grid(row=4,column=1, sticky=W)
		
		self.con_var = IntVar()
		self.con_var.set(1)
		self.net_var = IntVar()
		self.net_var.set(0)
		
		def con_m():
			self.net_var.set(0)
			self.con_var.set(1)
		def net_m():
			self.net_var.set(1)
			self.con_var.set(0)
					
		self.con = Checkbutton(self.settings_frame, text="Compute consensus tree (-con)", variable=self.con_var, command=con_m)
		self.con.grid(row=5,column=1, sticky=W)
		self.net = Checkbutton(self.settings_frame, text="Compute consensus network (-net)", variable=self.net_var, command=net_m)
		self.net.grid(row=6,column=1, sticky=W)
		
		self.minsup = Label(self.settings_frame, text="Specify minimum threshold (between 0 and 1) to keep branches in the consensus tree. For Majority rule consensus set to 0.5. Default: 0, extended majority-rule consensus (-minsup):", wraplength=500)
		self.minsup.grid(row=7,column=1, sticky=W, columnspan=5)
		
		self.minsup_entry = Entry(self.settings_frame, width=4)
		self.minsup_entry.insert(END, 0)
		self.minsup_entry.grid(row=8,column=1, sticky=W+N)
		
		self.bi = Label(self.settings_frame, text="Specify burn-in (no. of trees to be ignored, -bi):")
		self.bi.grid(row=9,column=1, sticky=W, columnspan=2)
		
		self.bi_entry = Entry(self.settings_frame, width=4)
		self.bi_entry.insert(END, 0)
		self.bi_entry.grid(row=9,column=3, sticky=W+N)
		
		self.sup = Label(self.settings_frame, text="Specify target tree onto which support will be mapped (-sup):")
		self.sup.grid(row=10,column=1, sticky=W, columnspan=5)
		self.sup_button = Button(self.settings_frame, text="Load", command=self.load_target_tree)
		self.sup_button.grid(row=10,column=5, sticky=W)
		self.sup_label = Label(self.settings_frame, text="no target tree specified", wraplength=500)
		self.sup_label.configure(foreground="grey")
		self.sup_label.grid(row=11,column=1, sticky=W, columnspan=5)
		
		self.settings_frame.rowconfigure(12, minsize=20)
		self.description_target = Label(self.settings_frame,text="Options only relevant when target tree is specified:")
		self.description_target.configure(font="Helvetica 12 bold")
		self.description_target.grid(row=13,column=1, sticky=W, columnspan=5)

		self.suptag = Label(self.settings_frame, text="Specify name of a node in -sup target tree. The corresponding node will then be assigned with IDs of trees where this node appears. Special option ALL will assign such IDs for all nodes of the target tree. (-suptag):", wraplength=500)
		self.suptag.grid(row=14,column=1, sticky=W, columnspan=5)
		self.suptag_entry = Entry(self.settings_frame, width=5)
		self.suptag_entry.grid(row=15,column=1, sticky=W+N)
		
		self.scale = Label(self.settings_frame, text="Set scaling factor for support values (default = percent, -scale):")
		self.scale.grid(row=16,column=1, sticky=W, columnspan=5)
		self.scale_entry = Entry(self.settings_frame, width=5)
		self.scale_entry.insert(END,100)
		self.scale_entry.grid(row=16, column=5, sticky=W+N)
		
		self.prec = Label(self.settings_frame, text="Set precision for support values (-prec):")
		self.prec.grid(row=17,column=1, sticky=W, columnspan=5)
		self.prec_entry = Entry(self.settings_frame, width=5)
		self.prec_entry.insert(END, 0)
		self.prec_entry.grid(row=17, column=5, sticky=W+N)
		
		def create_consensus():
			print(self.settings)
			cmd = self.settings.iqtree_path
			if self.filename == "":
				tkinter.messagebox.showinfo("No trees", "You need to specify a file with trees to ccompute a consensus tree.")
				return
			else:
				cmd += " -t %s" % self.filename
			if self.con_var.get() == 1:
				cmd += " -con"
			if self.net_var.get() == 1:
				cmd += " -net"
			try:
				minsup = float(self.minsup_entry.get())
				if minsup < 0 and minsup > 1:
					tkinter.messagebox.showinfo("minsup", "Specified value for -minsup is wrong.\nAllowed are values between 0 and 1.")
					return
				else:
					cmd += " -minsup %s" % str(minsup).rstrip("0").rstrip(".")
			except:
				tkinter.messagebox.showinfo("minsup", "Specified value for -minsup is wrong.\nAllowed are values between 0 and 1.")
				return
			try:
				bi = int(self.bi_entry.get())
				if bi > 0:
					cmd += " -bi %d" % bi
			except:
				tkinter.messagebox.showinfo("bi", "Specified value for -bi is wrong.\nAllowed are integer values.")
				return
			if self.target_filename != "":
				cmd += " -sup %s" % self.target_filename
				if self.suptag_entry.get() != "":
					cmd += " -suptag %s" % self.suptag_entry.get()
				try:
					scale = int(self.scale_entry.get())
					cmd += " -scale %d" % scale
				except:
					tkinter.messagebox.showinfo("scale", "Specified value for -scale is wrong.\nAllowed are integer values.")
					return
				try:
					prec = float(self.prec_entry.get())
					cmd += " -prec %d" % prec
				except:
					tkinter.messagebox.showinfo("prec", "Specified value for -prec is wrong.\nAllowed are numbers.")
					return
			print(cmd)
			self.spawn_iqtree_subprocess(cmd, self.settings)
			
		self.apply_button = Button(self.settings_frame, text="Compute Consensus tree", command=create_consensus)
		self.apply_button.grid(row=19, column=12, sticky=W)
		self.cancel_button = Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=W)
		
		self.settings_frame.grid()