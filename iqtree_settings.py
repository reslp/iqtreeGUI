#! /usr/bin/env python
# tkinter window for settings
# written by Philipp Resl
import os
import tkinter as tk
import tkinter.ttk
import tkinter.filedialog, tkinter.messagebox

class IQtreeSettingsWindow():
	filename = ""
	
	def load_tree(self):
		self.filename = tkinter.filedialog.askopenfilename(initialdir = "~",title = "Select starting tree")
		self.start_tree_path.grid(row=3,column=3, sticky=tk.W)
		self.start_tree_path.configure(text=self.filename)
		
	def __init__(self, master, data):
		self.master = master
		self.master.title("IQtree settings")
		self.settings_frame = tk.Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = tk.Label(self.settings_frame,text="IQtree general settings (none of these need to be changed)", justify=tk.LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=20)
		
		self.bionj=tk.IntVar()
		self.bionj.set(data.bionj_tree)
		self.random=tk.IntVar()
		self.random.set(data.random_tree)
		self.tree=tk.IntVar()
		self.tree.set(data.t)
		
		def bionj_cmd():
			if self.random.get() == 1:
				self.random.set(0)	
			if self.tree.get() == 1:
				self.tree.set(0)
			self.start_tree_button.grid_forget()
			self.start_tree_path.grid_forget()
				
		def random_cmd():
			if self.bionj.get() == 1:
				self.bionj.set(0)
			if self.tree.get() == 1:
				self.tree.set(0)
			self.start_tree_button.grid_forget()
			self.start_tree_path.grid_forget()	
		
		def tree_cmd():
			if self.tree.get() == 1:
				self.start_tree_button.grid(row=3,column=2, sticky=tk.W)
				if self.bionj.get() == 1:
					self.bionj.set(0)
				if self.random.get() == 1:
					self.random.set(0)
			if self.tree.get() == 0:
				self.start_tree_button.grid_forget()
			

		self.start_tree_label = tk.Checkbutton(self.settings_frame, text="Specify starting tree (-t): ", justify=tk.LEFT, variable=self.tree, command=tree_cmd)
		self.start_tree_label.grid(row=3,column=1, sticky=tk.W)
		self.start_tree_button = tk.Button(self.settings_frame, text="Load tree", command=self.load_tree)
		
		self.start_tree_path = tk.Label(self.settings_frame)
		self.start_tree_path.grid(row=3,column=3, sticky=tk.W, columnspan=5)
		self.start_tree_path.configure(text=data.starting_tree)
		self.start_tree_path.grid_forget()
		
	
		
		self.bionjm = tk.Checkbutton(self.settings_frame, text="Start with BIONJ tree (-t BIONJ)", variable=self.bionj, command=bionj_cmd)
		self.bionjm.grid(row=4, column=1, sticky=tk.W, columnspan=5)
		self.randomm = tk.Checkbutton(self.settings_frame, text="Start with RANDOM tree (-t RANDOM)", variable=self.random, command=random_cmd)
		self.randomm.grid(row=5, column=1, sticky=tk.W, columnspan=5)
		
		self.calc_fixed_user =tk.IntVar()
		self.calc_fixed_user.set(data.te)
		self.calculate_fixed = tk.Checkbutton(self.settings_frame, text="Only calculate likelihood of fixed user tree (-te)", variable=self.calc_fixed_user)
		self.calculate_fixed.grid(row=6, column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(7, minsize=20)
		
		self.outgroup_label = tk.Label(self.settings_frame, text="Manually specify outgroup Sequence (-o):\n(Must be a Sequence ID from alignment) ", justify=tk.LEFT)
		self.outgroup_label.grid(row=8, column=1, sticky=tk.W+tk.N)
		self.outgroup_entry = tk.Entry(self.settings_frame)
		self.outgroup_entry.insert(tk.END, data.o)
		self.outgroup_entry.grid(row=8,column=2, sticky=tk.W+tk.N)
		
		self.settings_frame.rowconfigure(9, minsize=20)
		
		self.outprefix_label = tk.Label(self.settings_frame, text="Prefix for Output file (-pre): ", justify=tk.LEFT)
		self.outprefix_label.grid(row=10, column=1, sticky=tk.W+tk.N)
		self.outprefix_entry = tk.Entry(self.settings_frame)
		self.outprefix_entry.insert(tk.END, data.pre)
		self.outprefix_entry.grid(row=10,column=2, sticky=tk.W+tk.N)
		
		self.seed_label = tk.Label(self.settings_frame, text="Random seed (-seed): \n(used to recreate runs)", justify=tk.LEFT)
		self.seed_label.grid(row=11, column=1, sticky=tk.W+tk.N)
		self.seed_entry = tk.Entry(self.settings_frame)
		self.seed_entry.insert(tk.END, data.seed)
		self.seed_entry.grid(row=11,column=2, sticky=tk.W+tk.N)
		
		self.verbose = tk.IntVar()
		self.verbose.set(data.v)
		self.quiet = tk.IntVar()
		self.quiet.set(data.quiet)
		
		def verbose_cmd():
			if self.quiet.get() == 1:
				self.quiet.set(0)
				
		def quiet_cmd():
			if self.verbose.get() == 1:
				self.verbose.set(0)
				
		self.settings_frame.rowconfigure(12, minsize=20)
		
		self.verbosem = tk.Checkbutton(self.settings_frame, text="Use verbose mode (-v)", variable=self.verbose, command=verbose_cmd)
		self.verbosem.grid(row=13, column=1, sticky=tk.W, columnspan=5)
		self.quietm = tk.Checkbutton(self.settings_frame, text="Use quiet mode (-quiet)", variable=self.quiet, command=quiet_cmd)
		self.quietm.grid(row=14, column=1, sticky=tk.W, columnspan=5)

		self.settings_frame.rowconfigure(15, minsize=20)

		self.save = tk.IntVar()
		self.save.set(data.save)
		self.savem = tk.Checkbutton(self.settings_frame, text="Use safe calculation to prefent numerical underflow (-save)", variable=self.save)
		self.savem.grid(row=16, column=1, sticky=tk.W, columnspan=5)
		self.ident = tk.IntVar()
		self.ident.set(data.keep_ident)
		self.identm = tk.Checkbutton(self.settings_frame, text="Keep identical sequences (-ident)", variable=self.ident)
		self.identm.grid(row=17, column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(18, minsize=20)
		
		def apply():
			try:
				if self.tree.get() == 1:
					data.starting_tree = self.start_tree_path.cget("text")
				else:
					data.starting_tree = "None"	
				data.bionj_tree = self.bionj.get()
				data.random_tree = self.random.get()
				data.o = self.outgroup_entry.get()
				data.pre = self.outprefix_entry.get()
				if self.seed_entry.get() != "random":
					data.seed = int(self.seed_entry.get())
				data.v = self.verbose.get()
				data.quiet = self.quiet.get()
				data.save = self.save.get()
				data.keep_ident = self.ident.get()
				self.master.destroy()
			except ValueError:
				tkinter.messagebox.showinfo("Error", "Some of the entered values are incorrect")
		
		self.apply_button = tk.Button(self.settings_frame, text="Apply & Close", command=apply)
		self.apply_button.grid(row=19, column=12, sticky=tk.W)
		self.cancel_button = tk.Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=tk.W)
		
		self.settings_frame.grid()