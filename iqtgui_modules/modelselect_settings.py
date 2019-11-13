#! /usr/bin/env python
# tkinter window for treesearch settings
# written by Philipp Resl
import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog, tkinter.messagebox

class ModelselectionSettingsWindow():
	def __init__(self, master, data):
		self.master = master
		self.master.title("Model selection advanced settings")
		self.settings_frame = Frame(self.master)
		
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
	
		self.description = Label(self.settings_frame,text="Advanced settings for automatic model selection", justify=LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W, columnspan=5)
		
		self.settings_frame.rowconfigure(2, minsize=20)

		self.testonly_var = IntVar()
		self.testonly_var.set(data.testonly)
		
		self.testnewonly_var = IntVar()
		self.testnewonly_var.set(data.mf)
		
		self.testnew_var = IntVar()
		self.testnew_var.set(data.mfp)
		
		self.test_var = IntVar()
		self.test_var.set(data.test)
		
		def testonly_m():
			self.testnewonly_var.set(0)
			self.testnew_var.set(0)
			self.test_var.set(0)
			self.testonly_var.set(1)	
		def test_m():
			self.testnewonly_var.set(0)
			self.testnew_var.set(0)
			self.test_var.set(1)
			self.testonly_var.set(0)
		def testnewonly_m():
			self.testnewonly_var.set(1)
			self.testnew_var.set(0)
			self.test_var.set(0)
			self.testonly_var.set(0)
		def testnew_m():
			self.testnewonly_var.set(0)
			self.testnew_var.set(1)
			self.test_var.set(0)
			self.testonly_var.set(0)
		
		self.testonly = Checkbutton(self.settings_frame, text="Perform Modeltest without tree building (-m TESTTONLY)", variable=self.testonly_var, command=testonly_m)
		self.testonly.grid(row=3,column=1, sticky=W, columnspan=5)
		
		self.test = Checkbutton(self.settings_frame, text="Perform Modeltest with tree building (-m TEST)", variable=self.test_var, command=test_m)
		self.test.grid(row=4,column=1, sticky=W, columnspan=5)

		self.testnewonly = Checkbutton(self.settings_frame, text="Perform extended model selection without tree building (-m MF)", variable=self.testnewonly_var, command=testnewonly_m)
		self.testnewonly.grid(row=5,column=1, sticky=W, columnspan=5)

		self.testnew = Checkbutton(self.settings_frame, text="Perform extended model selection with tree building (-m MFP)", variable=self.testnew_var, command=testnew_m)
		self.testnew.grid(row=6,column=1, sticky=W, columnspan=5)
		
		self.lm_label = Label(self.settings_frame, text="Additionally consider:")
		self.lm_label.grid(row=7,column=1, sticky=W)
		
		self.lm_options = ["no additional models","all Lie Markov models (+LM)","all Lie Markov models with RY symmetry (+LMRY) ","all Lie Markov models with WS symmetry (+LMWS)","all Lie Markov models with MK symmetry (+LMMK)","all strand-specific Lie Markov models (+LMSS)"]
		self.lm_var = StringVar()
		self.lm_var.set(self.lm_options[data.lm_type])
		self.which_lm_model = OptionMenu(self.settings_frame, self.lm_var,  *self.lm_options)
		self.which_lm_model.grid(row=7,column=2, sticky=W, columnspan=5)
		
		self.merge_var = IntVar()
		self.merge_var.set(data.merge)
		self.merge = Checkbutton(self.settings_frame, text="Merge partitions if possible (like PartitionFinder) (-merge)", variable=self.merge_var)
		self.merge.grid(row=8,column=1, sticky=W, columnspan=5)
		
		self.mset_label = Label(self.settings_frame, text="Restrict model search to models from (-mset):")
		self.mset_label.grid(row=9,column=1, sticky=W, columnspan=2)
		self.mset_options = ["all", "raxml", "phyml", "mrbayes"]
		self.mset_var = StringVar()
		self.mset_var.set(self.mset_options[data.mset])
		self.mset_menu = OptionMenu(self.settings_frame, self.mset_var,  *self.mset_options)
		self.mset_menu.grid(row=9,column=3,sticky=W)
		
		self.msub_label = Label(self.settings_frame, text="Restrict AA models to source (-msub):")
		self.msub_label.grid(row=10,column=1, sticky=W, columnspan=2)
		self.msub_options = ["all", "mitochondrial", "chloroplast", "nuclear", "viral"]
		self.msub_var = StringVar()
		self.msub_var.set(self.msub_options[data.msub])
		self.msub_menu = OptionMenu(self.settings_frame, self.msub_var,  *self.msub_options)
		self.msub_menu.grid(row=10,column=3,sticky=W)
		
		self.cmin_label = Label(self.settings_frame, text="Minimum number of categories for FreeRate model (-cmin): ", justify=LEFT)
		self.cmin_label.grid(row=11, column=1, sticky=W+N, columnspan=4)
		self.cmin_entry = Entry(self.settings_frame)
		self.cmin_entry.insert(END, data.cmin)
		self.cmin_entry.grid(row=11,column=5, sticky=W+N)
		
		self.cmax_label = Label(self.settings_frame, text="Maxmimum number of categories for FreeRate model (-cmax): ", justify=LEFT)
		self.cmax_label.grid(row=12, column=1, sticky=W+N, columnspan=4)
		self.cmax_entry = Entry(self.settings_frame)
		self.cmax_entry.insert(END, data.cmax)
		self.cmax_entry.grid(row=12,column=5, sticky=W+N)
		
		self.merit_options = ["all","AIC","AICc","BIC"]
		self.merit_var = StringVar()
		self.merit_var.set(self.merit_options[data.merit])
		self.merit_label = Label(self.settings_frame, text="Optimality criterion for model search (-merit):", justify=LEFT)
		self.merit_label.grid(row=13,column=1, sticky=W, columnspan=3)
		self.which_merit_model = OptionMenu(self.settings_frame, self.merit_var,  *self.merit_options)
		self.which_merit_model.grid(row=13,column=4, sticky=W)
		
		self.mtree_var = IntVar()
		self.mtree_var.set(data.mtree)
		self.mtree = Checkbutton(self.settings_frame, text="Turn on full model search for each model (-mtree)", variable=self.mtree_var)
		self.mtree.grid(row=14,column=1, sticky=W, columnspan=4)
		
		self.mredo_var = IntVar()
		self.mredo_var.set(data.mredo)
		self.mredo = Checkbutton(self.settings_frame, text="Ignore old model checkpoint file (-mredo)", variable=self.mredo_var)
		self.mredo.grid(row=15,column=1, sticky=W, columnspan=4)
		
		self.not_yet = Label(self.settings_frame,text="Functionality currently not implemented:\n -rcluster, -rclusterf, -rcluster-max, comma separated list of models in -mset, -mfreq,\n -mrate, -madd, -mdef", justify=LEFT)
		self.not_yet.configure(foreground="red")
		self.not_yet.grid(row=17,column=1, sticky=W, columnspan=5)
		
		def apply():
			print(data.__dict__)	
			try:
				print("a")
				data.testonly = self.testonly_var.get()
				data.test = self.test_var.get()
				data.mf = self.testnewonly_var.get()
				data.mfp = self.testnew_var.get()
				print("b")
				data.lm_type = self.lm_options.index(self.lm_var.get())
				data.merge = self.merge_var.get()
				data.mset = self.mset_options.index(self.mset_var.get())
				
				data.msub = self.msub_options.index(self.msub_var.get())
				data.cmin = int(self.cmin_entry.get())
				data.cmax = int(self.cmax_entry.get())
				data.merit = self.merit_options.index(self.merit_var.get())
				data.mtree = self.mtree_var.get()
				data.mredo = self.mredo_var.get()
				print(data.__dict__)				
				self.master.destroy()	
			except ValueError:
				tkinter.messagebox.showinfo("Error", "Some of the entered values are incorrect")
		
		self.apply_button = Button(self.settings_frame, text="Apply & Close", command=apply)
		self.apply_button.grid(row=19, column=12, sticky=W)
		self.cancel_button = Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=19, column=11, sticky=W)
		

		self.settings_frame.grid()