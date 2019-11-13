#! /usr/bin/env python
# tkinter window for treesearch settings
# written by Philipp Resl
import os
import tkinter as tk
import tkinter.ttk
import tkinter.filedialog, tkinter.messagebox

class TreesearchSettingsWindow():
	filename = ""
	
	def load_tree(self):
		self.filename = tkinter.filedialog.askopenfilename(initialdir = "~",title = "Select starting tree")
		self.start_tree_path.grid(row=3,column=2, sticky=tk.W)
		self.start_tree_path.configure(text=self.filename)
		
	def __init__(self, master, data):
		self.master = master
		self.master.title("Treesearch settings")
		self.settings_frame = tk.Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = tk.Label(self.settings_frame,text="Advanced settings of the tree search functionality", justify=tk.LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=tk.W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=30)
		
		self.allnni_var = tk.IntVar()
		self.allnni_var.set(data.allnni)
		self.allnni = tk.Checkbutton(self.settings_frame, text="Use thorough (but slower) NNI search (-allnni)", variable=self.allnni_var)
		self.allnni.grid(row=3,column=1, sticky=tk.W, columnspan=5)
		
		self.djc_var = tk.IntVar()
		self.djc_var.set(data.djc)
		self.djc = tk.Checkbutton(self.settings_frame, text="Avoid computing ML pairwise distances and BIONJ tree (-djc)", variable=self.djc_var)
		self.djc.grid(row=4,column=1, sticky=tk.W, columnspan=5)
		
		self.fast_var = tk.IntVar()
		self.fast_var.set(data.fast)
		self.fast = tk.Checkbutton(self.settings_frame, text="Use fast tree search mode (-fast)", variable=self.fast_var)
		self.fast.grid(row=5,column=1, sticky=tk.W, columnspan=5)
		
		self.ninit_label = tk.Label(self.settings_frame, text="Number of initial parsimony trees (-ninit): ", justify=tk.LEFT)
		self.ninit_label.grid(row=7, column=1, sticky=tk.W+tk.N)
		self.ninit_entry = tk.Entry(self.settings_frame)
		self.ninit_entry.insert(tk.END, data.ninit)
		self.ninit_entry.grid(row=7,column=2, sticky=tk.W+tk.N)
		
		self.n_label = tk.Label(self.settings_frame, text="Number of iterations to stop (-n): ", justify=tk.LEFT)
		self.n_label.grid(row=8, column=1, sticky=tk.W+tk.N)
		self.n_entry = tk.Entry(self.settings_frame)
		self.n_entry.insert(tk.END, data.n)
		self.n_entry.grid(row=8,column=2, sticky=tk.W+tk.N)
		
		self.ntop_label = tk.Label(self.settings_frame, text="Number of top initial parsimony trees (-ntop): ", justify=tk.LEFT)
		self.ntop_label.grid(row=9, column=1, sticky=tk.W+tk.N)
		self.ntop_entry = tk.Entry(self.settings_frame)
		self.ntop_entry.insert(tk.END, data.ntop)
		self.ntop_entry.grid(row=9,column=2, sticky=tk.W+tk.N)
		
		self.nbest_label = tk.Label(self.settings_frame, text="Number of trees in candidate set for ML search (-nbest): ", justify=tk.LEFT)
		self.nbest_label.grid(row=10, column=1, sticky=tk.W+tk.N)
		self.nbest_entry = tk.Entry(self.settings_frame)
		self.nbest_entry.insert(tk.END, data.nbest)
		self.nbest_entry.grid(row=10,column=2, sticky=tk.W+tk.N)
		
		self.nstop_label = tk.Label(self.settings_frame, text="Number of unsuccessful iterations to stop (-nstop): ", justify=tk.LEFT)
		self.nstop_label.grid(row=11, column=1, sticky=tk.W+tk.N)
		self.nstop_entry = tk.Entry(self.settings_frame)
		self.nstop_entry.insert(tk.END, data.nstop)
		self.nstop_entry.grid(row=11,column=2, sticky=tk.W+tk.N)
		
		self.pers_label = tk.Label(self.settings_frame, text="Pertubation strength (-pers): ", justify=tk.LEFT)
		self.pers_label.grid(row=12, column=1, sticky=tk.W+tk.N)
		self.pers_entry = tk.Entry(self.settings_frame)
		self.pers_entry.insert(tk.END, data.pers)
		self.pers_entry.grid(row=12,column=2, sticky=tk.W+tk.N)
		
		self.sprrad_label = tk.Label(self.settings_frame, text="SPR radius for initial parsimony tree search (-sprrad): ", justify=tk.LEFT)
		self.sprrad_label.grid(row=13, column=1, sticky=tk.W+tk.N)
		self.sprrad_entry = tk.Entry(self.settings_frame)
		self.sprrad_entry.insert(tk.END, data.sprrad)
		self.sprrad_entry.grid(row=13,column=2, sticky=tk.W+tk.N)
		
		
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
		
		self.apply_button = tk.Button(self.settings_frame, text="Apply & Close", command=apply)
		self.apply_button.grid(row=19, column=12, sticky=tk.W)
		self.cancel_button = tk.Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=tk.W)
		
		self.settings_frame.grid()