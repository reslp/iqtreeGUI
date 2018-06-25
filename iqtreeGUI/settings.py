#! /usr/bin/env python
# tkinter window for settings
# written by Philipp Resl
import ConfigParser
import tkFileDialog
import os
import sys

try:
	import Tkinter as tk
except ImportError:
	import tkinter as tk

try:
	import ttk
	py3 = 0
	from Queue import Queue, Empty
except ImportError:
	import tkinter.ttk as ttk
	from queue import Queue, Empty
	py3 = 1
	
def resource_path(relative):
	if hasattr(sys, '_MEIPASS'):
		return sys._MEIPASS + relative
	else:
		return sys.path[0] + relative

	
class SettingsWindow():	
	def read_config_file(self):
		config = ConfigParser.ConfigParser()
		print self.master.config_path
		try:
			print self.config_file
			config.read(self.config_file)
			self.path_iq = config.get('Settings', 'iqtree')
			self.version = config.get('Settings', 'version')
			self.path_wd = config.get('Settings', 'wd')
		except:
			print "read error"
			#ttk.tkMessageBox.showerror("Error", "Config file error")
			
	def load_iqtree(self):
		filename = tkFileDialog.askopenfilename(initialdir = "~",title = "Select IQ-Tree executable")
		self.iqtree_path_entry.delete(0, tk.END)
		self.iqtree_path_entry.insert(tk.END, filename)
		self.path_iq = filename
	
	def load_wd(self):
		dirname = tkFileDialog.askdirectory(initialdir = "~",title = "Select working directory")
		self.wd_entry.delete(0, tk.END)
		self.wd_entry.insert(tk.END, dirname)
		self.path_wd = dirname
			
	def __init__(self, master, data, file_path):
		self.config_file = file_path
		self.master = master
		self.master.title("IQ-Tree GUI Settings")
		self.settings_frame = tk.Frame(self.master)
		#create an empty margin so that the widgets wont stick to the very edges
		self.settings_frame.rowconfigure(0, minsize=30)
		self.settings_frame.rowconfigure(20, minsize=30)
		self.settings_frame.columnconfigure(0, minsize=30)
		self.settings_frame.columnconfigure(20, minsize=30)
	
		self.description = tk.Label(self.settings_frame,text="Some basic IQtree GUI settings:", justify=tk.LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=tk.W, columnspan=5)
		self.settings_frame.rowconfigure(2, minsize=30)
		
		#self.read_config_file()
		self.label= tk.Label(self.settings_frame, text="Path to iqtree:")
		self.label.grid(row=3, column=1)
		self.iqtree_path_entry = tk.Entry(self.settings_frame)
		self.iqtree_path_entry.insert(tk.END, data.iqtree_path)
		self.iqtree_path_entry.grid(row=3, column=2)
		self.change_but = tk.Button(self.settings_frame, text="Change", command=self.load_iqtree)
		self.change_but.grid(row=3, column=3)
		
		self.label_wd = tk.Label(self.settings_frame, text="Working directory: Directory of alignment")
		self.label_wd.grid(row=4,column=1, columnspan=2, sticky=tk.W)

		
		"""
		# this is currently not working, iqtree seems to produce output in the alignment directory
		self.wd_entry = tk.Entry(self.settings_frame)
		self.wd_entry.insert(tk.END, data.wd)
		self.change_but_wd = tk.Button(self.settings_frame, text="Change", command=self.load_wd)
		self.wd_entry.grid(row=2,column=2)
		self.change_but_wd.grid(row=2, column=3)
		"""
		
		def set_config_file():
			data.iqtree_path = self.iqtree_path_entry.get()
			#data.wd = self.wd_entry.get()
			config = ConfigParser.ConfigParser()
		
			configfile = open(self.config_file, 'wb')
			config.add_section('Settings')
			config.set('Settings', 'iqtree', data.iqtree_path)
			#config.set('Settings', 'wd', data.wd)
			config.set('Settings', 'version', data.version)
		
			config.write(configfile)
			configfile.close()
			self.master.destroy()

		self.settings_frame.rowconfigure(9, minsize=20)
		self.apply_change = tk.Button(self.settings_frame, text="Apply & Close", command=set_config_file)
		self.apply_change.grid(row=10, column=4, sticky=tk.W)
		
		self.cancel_button = tk.Button(self.settings_frame, text="Cancel", command=self.master.destroy)
		self.cancel_button.grid(row=10, column=5, sticky=tk.W)
		

		
		
		self.settings_frame.grid()

		