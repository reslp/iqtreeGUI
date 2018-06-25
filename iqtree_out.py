#! /usr/bin/env python
# tkinter Frame for partition selection
# written by Philipp Resl
# thanks to StackOverflow User jfs: https://stackoverflow.com/questions/665566/redirect-command-line-results-to-a-tkinter-gui
import sys, os
from ScrollableFrame import *
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from ScrolledText import ScrolledText
import shlex
import itertools
import signal

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
	
def iter_except(function, exception):
    try:
        while True:
            yield function()
    except exception:
        return


class IqtreeWindow():
	displayed_output =""
	command = ""
	partition_command = ""
	wd = "~"
	
	def jump_to_selection(self, ef):
		selection = self.checkpoints.curselection()
		#print selection[0]
		line = self.checkpoints_dict[self.checkpoints.get(selection[0])]
		print line
		self.output_label.mark_set("section", "%s.1"%line)
		self.output_label.see("section")
		
	def __init__(self, master, settings):
		self.settings = settings
		self.master = master
		self.master.protocol( "WM_DELETE_WINDOW", self.close)
		self.master.title("iqtree Output")
		self.checkpoints = Listbox(self.master)
		self.checkpoints.grid(column=1,row=1, sticky=N+W+S)
		#self.checkpoints.bind("<Button-1>", self.jump_to_selection)
		self.checkpoints.bind("<<ListboxSelect>>", self.jump_to_selection)
		self.output_label = ScrolledText(self.master)
		self.output_label.grid(column=2,row=1)
		self.save_button = Button(self.master, text="Save Output")
		self.save_button.grid(column=1,row=2)
		self.line_number = 0
		self.checkpoints_dict = {}
		self.checkpoints_dict["Start of run"] = self.line_number
		self.checkpoints.insert(END, "Start of run")
		
	
	def display(self, text):
		self.line_number += 1
		self.displayed_output = str(self.line_number) + " " + text
		self.output_label.insert(tk.END,self.displayed_output)
		self.output_label.see(tk.END)
		if self.displayed_output.startswith("IQ-TREE"):
			self.checkpoints.insert(END, "IQ-TREE")
			self.checkpoints_dict["IQ-TREE"] = self.line_number
		if self.displayed_output.startswith("ModelFinder"):
			self.checkpoints.insert(END, "ModelFinder")
			self.checkpoints_dict["ModelFinder"] = self.line_number	
		if self.displayed_output.startswith("Akaike Information Criterion:"):
			self.checkpoints.insert(END, "Best Model")
			self.checkpoints_dict["Best Model"] = self.line_number
		if "INITIALIZING CANDIDATE TREE SET" in self.displayed_output:
			self.checkpoints.insert(END, "Initialize tree")
			self.checkpoints_dict["Initialize tree"] = self.line_number
		if "OPTIMIZING CANDIDATE TREE SET" in self.displayed_output:
			self.checkpoints.insert(END, "Optimize tree")
			self.checkpoints_dict["Optimize tree"] = self.line_number
		if "FINALIZING TREE SEARCH" in self.displayed_output:
			self.checkpoints.insert(END, "Finalize tree")
			self.checkpoints_dict["Finalize tree"] = self.line_number
		#print self.checkpoints_dict
		#self.frame.configure(text=self.displayed_output)
	
	def send_command(self, command):
		self.command = command
	
	def send_partitions(self, partition_command):
		self.partition_command = partition_command
		
	def spawn_process(self):
		print "Command is:", self.command
		cmd_list = shlex.split(self.command)
		print "Command list:", cmd_list
		cmd_list[0] = "~/bin/iqtree"
		print "Command list:", cmd_list
		self.process = Popen(self.command, stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=True, cwd=self.settings.wd)
		#self.process = Popen("iqtree", stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=False, cwd=self.settings.wd)

		q = Queue(maxsize=1024)
		t = Thread(target=self.reader_thread, args=[q])
		t.deamon= True
		t.start()
		self.update(q)

		
	def reader_thread(self, q):
		# Read subprocess output and put it into the queue.
		print "READING"
		try:
			with self.process.stdout as pipe:
				for line in iter(pipe.readline, b''):
					q.put(line)
		finally:
			q.put(None)
		try:
			with self.process.stderr as pipe:
				for line in iter(pipe.readline, b''):
					q.put(line)
		finally:
			q.put(None)
		

	def update(self, q):
		# Update GUI with items from the queue.
		for line in iter_except(q.get_nowait, Empty): # display all content
			if line is None:
				#self.quit()
				return
			else:
				self.display(line) # update GUI
				break # display no more than one line per 40 milliseconds
		self.master.after(40, self.update, q) # schedule next update
		
	def close(self):
		self.process.kill()
		self.master.destroy()
		
		