#! /usr/bin/env python
# iqtree output window
# written by Philipp Resl
# thanks to StackOverflow User jfs: https://stackoverflow.com/questions/665566/redirect-command-line-results-to-a-tkinter-gui
import sys, os

from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from queue import Queue, Empty
from iqtgui_modules import ScrollableFrame
import shlex
import itertools
import signal
import platform
import time

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
	
		
	def __init__(self, master, settings):
		self.settings = settings
		self.master = master
		self.master.resizable(False, False)
		self.master.protocol( "WM_DELETE_WINDOW", self.close)
		self.master.title("iqtree Output")
		self.checkpoints = Listbox(self.master)
		self.checkpoints.grid(column=1,row=1, sticky=N+W+S)
		#self.checkpoints.bind("<Button-1>", self.jump_to_selection)
		self.checkpoints.bind("<<ListboxSelect>>", self.jump_to_selection)
		self.output_label = ScrolledText(self.master, font=("Helvetica", 10), width=100)
		self.output_label.grid(column=2,row=1)
		self.save_button = Button(self.master, text="Save Output")
		self.save_button.grid(column=1,row=2)
		
		def cancel():
			self.process.kill()
			self.display("RUN CANCELED BASED ON USER REQUEST")
		
		self.cancel = Button(self.master, text="Cancel Run", command=cancel)
		self.cancel.grid(column=2,row=2)
		
		
		
		self.line_number = 0
		self.checkpoints_dict = {}
		self.checkpoints_dict["Start of run"] = self.line_number
		self.checkpoints.insert(END, "Start of run")
		self.n_empty_lines = 0
		
	def jump_to_selection(self, ef):
		selection = self.checkpoints.curselection()
		line = self.checkpoints_dict[self.checkpoints.get(selection[0])]
		print(line)
		self.output_label.mark_set("section", "%s.1"%line)
		self.output_label.see("section")

	def display(self, text):
		if text == "":
			self.n_empty_lines += 1
		if self.n_empty_lines >= 10:
			self.process.kill()
		else:
			self.line_number += 1
			self.displayed_output = str(self.line_number) + " " + text
			self.displayed_output = " " + text
			self.output_label.insert(END,self.displayed_output)
			self.output_label.see(END)
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
		print("Command is:", self.command)
		#cmd_list = shlex.split(self.command)
		if "Windows" in platform.system():
			separator="\\"
		else:
			separator="/"
		os.chdir(self.settings.wd + separator + self.settings.analysisname)
		self.process = Popen(self.command, stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=True)

		self.q = Queue(maxsize=1024)
		self.t = Thread(target=self.reader_thread, args=[self.q])
		self.t.setDaemon(True)
		self.t.start()
		self.update(self.q)

	def reader_thread(self, q):
		# Read subprocess output and put it into the queue.
		print("READING")
		try:
			with self.process.stdout as pipe:
				for line in iter(pipe.readline, b''):
					q.put(line)
		finally:
			q.put(None)
			self.process.kill()
		try:
			with self.process.stderr as pipe:
				for line in iter(pipe.readline, b''):
					q.put(line)
		finally:
			q.put(None)
			self.process.kill()
		

	def update(self, q):
		# Update GUI with items from the queue.
		for line in iter_except(q.get_nowait, Empty): # display all content
			if line is None:
				#self.quit()
				return
			else:
				self.display(line) # update GUI
				break # display no more than one line per 40 milliseconds
		self.master.after(20, self.update, q) # schedule next update
		
	def close(self):
		self.process.kill()
		self.master.destroy()

		
		