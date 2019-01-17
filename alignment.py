#! /usr/bin/env python
# tkinter Frame for importing multiple alignments
# written by Philipp Resl
from alignment_view import *
from tkinter import *
import tkinter.ttk as ttk

class Alignment(Frame):
	alignment_id = ""
	alignment_path = ""
	window = ""
	def show_alignment(self):
		self.window = Toplevel()
		self.al_window = AlignmentView(self.window, alignment=self.alignment_id, filename=self.alignment_path)
		self.master.wait_window(self.al_window)
	
	def remove_alignment(self):
		#print("Length of alignment list before: %s" % len(self.al_list))
		for no in range(0,len(self.al_list)):
			self.al_list[no].grid_forget()
		
		del self.al_list[self.alignment_no-1]
		#print("Length of alignment list after: %s" % len(self.al_list))
		for no in range(0,len(self.al_list)):
			#self.al_list[no].grid_forget()
			#print("Alignment %s is now %s" % (str(self.al_list[no].alignment_no), str(no+1)))
			self.al_list[no].alignment_no = no + 1
			self.al_list[no].alignment_label.configure(text="Alignment "+str(no+1)+": ")
			self.al_list[no].alignment_label.configure(font=("TkTextFont", 12, "bold"))
			self.al_list[no].grid(sticky=W)
			self.al_list[no].update()
		#kill the alignment window if present, need to find a better way of doing this
		if isinstance(self.window,str) == False and Toplevel.winfo_exists(self.window)==1: 
			self.window.destroy()
		self.info_lab.config(text="Alignments: %s Alignment(s) loaded" % str(len(self.al_list)))
		#print(self.nametowidget(self))
		
		#print(len(self.al_list))


		#self.master.master.master.master.master.update_idletasks()
		#print(dir(self.master.winfo_toplevel()))
		
		self.destroy()
		
	def create_widgets(self):
		self.alignment_label = Label(self, text=self.alignment_id)
		self.alignment_label.grid(row=0,column=3)
		self.alignment_label.configure(font=("TkTextFont", 12, "bold"))
		self.alignment_path_label = Label(self, text=self.alignment_path)
		self.alignment_path_label.grid(row=0,column=4)
		self.view_button = Button(self, text="View", command=self.show_alignment)
		self.view_button.grid(row=0,column=1)
		self.remove_button = Button(self, text="Remove", command=self.remove_alignment)
		self.remove_button.grid(row=0,column=2)
		print("Alignment created: %s" % self.alignment_no)
		
	def __init__(self, master, align_id, path, number, alignment_list, info_label):
		Frame.__init__(self, master)
		self.info_lab = info_label
		self.al_list = alignment_list
		self.master = master
		self.alignment_id = align_id
		self.alignment_path = path
		self.alignment_no = number
		self.create_widgets()