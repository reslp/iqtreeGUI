#! /usr/bin/env python
# tkinter window for settings
# written by Philipp Resl
import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog, tkinter.messagebox

class AdvancedBSWindow():
	wbtvar = 0
	wbtlvar = 0
	def __init__(self, master, data):
		self.master = master
		self.master.title("Advanced Bootstrap settings")
		self.settings_frame = Frame(self.master)
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
		
		self.description = Label(self.settings_frame,text="Here you can configure advanced options of the\nbootstraping functionality of iqtree", justify=LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W, columnspan=5)

		self.settings_frame.rowconfigure(2, minsize=20)
		
		self.bcor_label= Label(self.settings_frame,text="Minimum correlation coefficient for UFBoot: ")
		self.bcor_label.grid(row=3, column=1, sticky=W)
		self.bcor_entry = Entry(self.settings_frame)
		self.bcor_entry.insert(END,data.bcor)
		self.bcor_entry.grid(row=3, column=2, sticky=W)
		
		self.beps_label= Label(self.settings_frame,text="Epsilon to break tie in RELL: ")
		self.beps_label.grid(row=4, column=1, sticky=W)
		self.beps_entry = Entry(self.settings_frame)
		self.beps_entry.insert(END,data.beps)
		self.beps_entry.grid(row=4, column=2, sticky=W)
		
		self.nm_label= Label(self.settings_frame,text="Maximum number of iterations to stop: ")
		self.nm_label.grid(row=5, column=1, sticky=W)
		self.nm_entry = Entry(self.settings_frame)
		self.nm_entry.insert(END,data.nm)
		self.nm_entry.grid(row=5, column=2, sticky=W)
		
		self.nstep_label= Label(self.settings_frame,text="Iteration interval to check for\nUFBoot convergence: ")
		self.nstep_label.grid(row=6, column=1, sticky=W)
		self.nstep_entry = Entry(self.settings_frame)
		self.nstep_entry.insert(END,data.nstep)
		self.nstep_entry.grid(row=6, column=2, sticky=W)
		
		self.settings_frame.rowconfigure(8, minsize=20)
		
		self.bbnivar = IntVar()
		self.bbnivar.set(data.bnni)
		
		def bbni():
			self.bbnivar.set(1)
		
		
		self.bbni = Checkbutton(self.settings_frame, text="reduce model violation (-bnni)", command=bbni, variable=self.bbnivar)
		self.bbni.grid(row=9, column=1, sticky=W)

		
		self.wbtvar = IntVar()
		self.wbtlvar = IntVar()
		
		self.wbtvar.set(data.wbt)
		self.wbtlvar.set(data.wbtl)
		
		def wbt():
			if self.wbtlvar.get() == 1:
				self.wbtlvar.set(0)
			print() #change!!
			
		self.wbt = Checkbutton(self.settings_frame, text="Write bootstrap trees to .ufboot file. (-wbt)", command=wbt, variable=self.wbtvar)
		self.wbt.grid(row=10, column=1, sticky=W)
		
		
		def wbtl():
			if self.wbtvar.get() == 1:
				self.wbtvar.set(0)
			print() #change!!
		
		
		self.wbtl = Checkbutton(self.settings_frame, text="Write bootstrap trees to .ufboot file\nincluding branch lengths. (-wbtl)", command=wbtl, variable=self.wbtlvar)
		self.wbtl.grid(row=11, column=1, sticky=W)
		
		def apply():
			try:
				data.bnni = self.bbnivar.get()
				data.beps = float(self.beps_entry.get())
				data.bcor = float(self.bcor_entry.get())
				data.nm = int(self.nm_entry.get())
				data.nstep = int(self.nstep_entry.get())
				data.wbt = self.wbtvar.get()
				data.wbtl = self.wbtlvar.get()
				self.master.destroy()
				
			except ValueError:
				tkinter.messagebox.showinfo("Error", "Some of the entered values are incorrect")
		
		self.apply_button = Button(self.settings_frame, text="Apply & Close", command=apply)
		self.apply_button.grid(row=11, column=12, sticky=W)
		self.cancel_button = Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=11, column=11, sticky=W)
		self.settings_frame.grid()
		
		