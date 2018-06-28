#!/usr/bin/env python
#written by Philipp Resl

import sys, os
import subprocess
import multiprocessing
import tempfile
from subprocess import Popen, PIPE
import datetime
import ConfigParser
import xml.etree.ElementTree as ET
from xml.dom import minidom as MD
import unicodedata
from Tkinter import *
import tkFileDialog, tkMessageBox
from ScrolledText import ScrolledText
import ttk
import platform


from os.path import expanduser
"""
try:
	from Tkinter import *
	import tkFileDialog, tkMessageBox
	from ScrolledText import ScrolledText
except ImportError:
	from tkinter import *

try:
	import ttk
	py3 = 0
except ImportError:
	import tkinter.ttk as ttk
	py3 = 1
"""
import iqtree_gui_support
from model_select import *
from partition import *
from ScrollableFrame import *
from iqtree_out import *
from settings import *
from advanced_bootstrap import *
from data_types_settings import *
from iqtree_settings import *
from treesearch_settings import *
from modelselect_settings import *
from consensustree import *
from robinsonfoulds import *
from randomtree import *
from alignment import *
"""
def vp_start_gui():
	# Starting point when module is the main routine.
	global val, w, root
	root = Tk()
	iqtree_gui_support.set_Tk_var()
	top = itree_GUI (root)
	iqtree_gui_support.init(root, top)
	root.mainloop()

w = None
def create_itree_GUI(root, *args, **kwargs):
	# Starting point when module is imported by another program.
	global w, w_win, rt
	rt = root
	w = Toplevel (root)
	iqtree_gui_support.set_Tk_var()
	top = itree_GUI (w)
	iqtree_gui_support.init(w, top, *args, **kwargs)
	return (w, top)

def destroy_itree_GUI():
	global w
	w.destroy()
	w = None
"""	
def resource_path(relative):
	if hasattr(sys, '_MEIPASS'):
		return sys._MEIPASS + relative
	return sys.path[0] + relative
	#return os.path.join(os.environ.get("_MEIPASS2",os.path.abspath(".")),relative)


		
		
###### start of main class #######
class iqtree_GUI:
	filename = "/Users/sinnafoch/Dropbox/Philipp/iqtreegui/test_cases/alignment_small.fas"
	#iqtree_path = "/usr/bin/iqtree"
	nthreads = "AUTO"
	nbootstrap = 1000
	overwrite=1
	simulate_only=1
	
	choice_bs_option = 1
	choice_part_option = 1
	choice_model_option = 1
	partition_model = ""
	
	model_partitions = []
	align_partitions = []
	alignments = []
	part_offset=0
	align_offset = 0
	nmodels = 1
	reduce_model_violation = 0
	
	command = ""
	partition_command = ""
	
	is_models_set = False
	
	# initialize advanced settings types
	advanced_bs_settings = BootstrapConfig()
	treesearch_settings = TreeSearchSettings()
	iqtree_settings = IQtreeSettings()
	gui_settings = IQtreeGUIConfig()
	advanced_model_settings	= AutomaticModelSelectionSettings()

	def convert_number(self, s): #function to distinguish between float, int and str when reading from xml file
		try:
			float(s)
			if float(s).is_integer():
				return int(s)
			else:
				return float(s)	
		except ValueError:
			return s
		

	def about_message(self):
		tkMessageBox.showinfo("About", "iqtreeGUI Version "+self.gui_settings.version+"\nwritten by Philipp Resl")
	
	def not_yet(self):
		tkMessageBox.showinfo("Info", "This feature is not yet implemented in IQ-tree GUI.")
		
	def save_analysis(self):
		f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".xml")
		if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
			return
		top = ET.Element('top')

		comment = ET.Comment('Generated for iqtreeGUI')
		top.append(comment)
		
		#write bootstrap settings
		child = ET.SubElement(top, "advancedbootstrap")
		for key, value in self.advanced_bs_settings.__dict__.iteritems():
			elem = ET.SubElement(child, key)
			elem.text = str(value)
		elem = ET.SubElement(child, "nbootstrap")
		elem.text = self.entry_bs.get()
		elem = ET.SubElement(child, "bootstrap_type")
		elem.text = str(self.choice_bs_option)
		
		#write tree search settings
		child = ET.SubElement(top, "treesearch")
		for key, value in self.treesearch_settings.__dict__.iteritems():
			elem = ET.SubElement(child, key)
			elem.text = str(value)
		
		#write iqtree settings
		child = ET.SubElement(top, "iqtreesettings")
		for key, value in self.iqtree_settings.__dict__.iteritems():
			elem = ET.SubElement(child, key)
			elem.text = str(value)
		elem = ET.SubElement(child, "redo")
		elem.text = str(self.overwrite)
			
		#write advanced model settings
		child = ET.SubElement(top, "advancedmodelsettings")
		for key, value in self.advanced_model_settings.__dict__.iteritems():
			elem = ET.SubElement(child, key)
			elem.text = str(value)
			
		#alignment
		child = ET.SubElement(top, "alignments")
		for alignment in self.alignments:
			elem = ET.SubElement(child, "filename")
			elem.text = alignment.alignment_path
		
		
		#for partitioned analysis
		part_child = ET.SubElement(top, "partitions")
		elem = ET.SubElement(part_child, "part_var")
		elem.text = str(self.part_var.get())
		if self.part_var.get() == 2: #if there are multiple partitions
			#partitions
			child = ET.SubElement(part_child, "partitionmodeltype")
			child.text = str(self.part_model_var.get())
			for i in range(0, len(self.align_partitions)):
				name = "partition%d" % i
				child = ET.SubElement(part_child, name)
				elem = ET.SubElement(child, "start")
				elem.text = str(self.align_partitions[i].get_start())
				elem = ET.SubElement(child, "end")
				elem.text = str(self.align_partitions[i].get_end())
				elem = ET.SubElement(child, "which_alignment")
				elem.text = str(self.align_partitions[i].get_which_alignment())
		else:
			child = ET.SubElement(part_child, "partition0")
			elem = ET.SubElement(child, "start")
			elem.text = str(0)
			elem = ET.SubElement(child, "end")
			elem.text = str("end")
			
		#models
		model_child = ET.SubElement(top, "models")
		elem = ET.SubElement(model_child, "model_var")
		elem.text = str(self.v_model_option.get())
		if self.v_model_option.get() == 2: #if model specification is set to manual
			for i in range(0, len(self.model_partitions)):
				name = "model%d" % i
				child = ET.SubElement(model_child, name)
				for key, value in self.model_partitions[i].model.__dict__.iteritems():
					elem = ET.SubElement(child, key)
					elem.text = value
		else:
			child = ET.SubElement(model_child, "model0")
			elem = ET.SubElement(child, "model")
			elem.text = str(self.v_model_option.get())
			
			
		child = ET.SubElement(top, "bootstrap")
		elem = ET.SubElement(child, "option")
		elem.text = str(self.v.get())
		elem = ET.SubElement(child, "nbootstrap")
		elem.text = self.entry_bs.get()

		#make output human readable
		output = ET.tostring(top, 'utf-8')
		reparsed_output = MD.parseString(output)
		
		f.write(reparsed_output.toprettyxml(indent="\t"))
		f.close()
		
	def load_analysis(self):
		print "loading analysis..."
		self.reset_partitions() # delete old partitions
		filename = tkFileDialog.askopenfilename()
		if filename is "": # return `None` if dialog closed with "cancel".
			return
		try:
			tree = ET.parse(filename) 
		except:
			tkMessageBox.showinfo("Error", "Not a valid XML file")
			return 
		root = tree.getroot()
		
		for child in root:
			if child.tag == "advancedbootstrap":
				for subelement in child:
					for key, setting in self.advanced_bs_settings.__dict__.iteritems():
						if key == subelement.tag:
							self.advanced_bs_settings.__dict__[key] = self.convert_number(subelement.text)
			if child.tag == "treesearch":
				for subelement in child:
					for key, setting in self.treesearch_settings.__dict__.iteritems():
						if key == subelement.tag:
							self.treesearch_settings.__dict__[key] = self.convert_number(subelement.text)
			if child.tag == "iqtreesettings":
				for subelement in child:
					for key, setting in self.iqtree_settings.__dict__.iteritems():
						if key == subelement.tag:
							self.iqtree_settings.__dict__[key] = self.convert_number(subelement.text)
			if child.tag == "advancedmodelsettings":
				for subelement in child:
					for key, setting in self.advanced_model_settings.__dict__.iteritems():
						if key == subelement.tag:
							#print key
							#print subelement.text
							self.advanced_model_settings.__dict__[key] = self.convert_number(subelement.text)
			if child.tag == "alignments": #adjust this for multiple alignment files
				print "loading alignments"
				for subelement in child:
					self.alignments.append(Alignment(self.alignment_scroll_frame, align_id="Alignment "+str(len(self.alignments)+1)+":  ", path = subelement.text, number=len(self.alignments)+1))
					self.alignments[-1].grid(sticky=W)
					self.align_offset += 30
				self.alignment_scroll_frame.update()
				self.alignment_info_label.config(text="Alignments: %s Alignment(s) loaded" % str(len(self.alignments)))	
			if child.tag == "partitions":
				self.part_set_frame_container.lift(self.partition_layer)
				self.button_create_part.lift(self.partition_layer)
				self.button_delete_part.lift(self.partition_layer)
				self.which_partition_model.lift(self.partition_layer)
				for subelement in child:
					if subelement.tag == "part_var":
						self.part_var.set(self.convert_number(subelement.text))
						self.choice_part_option = self.convert_number(subelement.text)
						if subelement.text=="1":
							self.part_set_frame_container.lower(self.partition_layer)
							self.button_create_part.lower(self.partition_layer)
							self.button_delete_part.lower(self.partition_layer)
							self.which_partition_model.lower(self.partition_layer)
							break
					elif subelement.tag == "partitionmodeltype":
						self.partition_model = subelement.text
						self.part_model_var.set(subelement.text)
					else:
						self.create_partition()
						for pos in subelement:
							#print pos.tag
							#print pos.text
							if pos.tag == "start":
								self.align_partitions[-1].start_entry.insert(0,pos.text)
							if pos.tag == "end":
								self.align_partitions[-1].end_entry.insert(0,pos.text)
							if pos.tag == "which_alignment":
								self.align_partitions[-1].part_alignment_var.set("Alignment " + pos.text)
								self.align_partitions[-1].which_alignment = "Alignment " + pos.text
			"""
			if child.tag == "models":
				i = 0
				for subelement in child:
					if subelement.tag == "model_var":
						self.v_model_option.set(subelement.text)
						self.choice_model_option = self.convert_number(subelement.text)
					else:
						for model in subelement:
							#print "iteration: ", i
							for key, setting in self.model_partitions[i].model.__dict__.iteritems():
								if key == model.tag:
									#print key, model.text
									self.model_partitions[i].model.__dict__[key] = self.convert_number(model.text)
							#print "length %d " % len(self.model_partitions)
						i += 1
						if i == len(self.model_partitions):
							break
				for i in range(0, len(self.model_partitions)):
					self.model_partitions[i].load_model()
				self.model_frame_down.grid(row=3, column=1, sticky=N+S+W+E)
				self.auto_model_select.grid_forget()
			"""
			if child.tag == "bootstrap":
				for subelement in child:
					if subelement.tag == "option":
						self.v.set(self.convert_number(subelement.text))
						self.choice_bs_option = self.convert_number(subelement.text)
					if subelement.tag == "nbootstrap":
						self.nbootstrap = self.convert_number(subelement.text)
						self.entry_bs.delete(0,END)
						self.entry_bs.insert(END, self.nbootstrap)
						
			"""for subelement in child:
				print subelement.tag, subelement.text
			"""
		
	
	def spawn_random_tree_window(self):
		random_window=Toplevel()
		random = RandomTreeWindow(random_window, self.gui_settings)
		self.master.wait_window(random_window)
	
	def spawn_consensus_tree_window(self):
		consensus_window=Toplevel()
		consensus = ConsensusTreeWindow(consensus_window, self.gui_settings)
		self.master.wait_window(consensus_window)
	
	def spawn_robionsonfoulds_window(self):
		robinson_window=Toplevel()
		robinson = RobinsonFouldsWindow(robinson_window, self.gui_settings)
		self.master.wait_window(robinson_window)
	
	def spawn_model_selection_window(self):
		settings_window=Toplevel()
		settings = ModelselectionSettingsWindow(settings_window, self.advanced_model_settings)
		self.master.wait_window(settings_window)
		
	
	def spawn_settings_window(self):
		print "settings"
		settings_window=Toplevel(self.master)
		settings = SettingsWindow(settings_window, self.gui_settings, self.config_path)
		self.master.wait_window(settings_window)
		self.read_config_file()
		# self.info_label.insert(END, self.get_time()+"New configuration file loaded\n")
		# self.info_label.insert(END, self.get_time()+"Path to iqtree is: "+self.gui_settings.iqtree_path+"\n")
	
	def spawn_advanced_bootstrap_window(self):
		print "advanced bootstrap settings"
		settings_window=Toplevel()
		settings = AdvancedBSWindow(settings_window, self.advanced_bs_settings)
		self.master.wait_window(settings_window)
		# self.info_label.insert(END, self.get_time()+"Advanced Bootstrap are: \n")
		# self.info_label.insert(END, "bcor=" + str(self.advanced_bs_settings.bcor) + ", beps=" + str(self.advanced_bs_settings.beps)+", nm=" + str(self.advanced_bs_settings.nm)+", nstep=" + str(self.advanced_bs_settings.nstep)+", bnni=" + str(self.advanced_bs_settings.bnni)+", wbt=" + str(self.advanced_bs_settings.wbt)+", wbtl=" + str(self.advanced_bs_settings.wbtl)+"\n")
	
	def spawn_iqtree_settings_window(self):
		settings_window=Toplevel()
		settings = IQtreeSettingsWindow(settings_window, self.iqtree_settings)
		self.master.wait_window(settings_window)
		# self.info_label.insert(END, self.get_time()+"IQTree settings are:\n")
		# self.info_label.insert(END, self.get_time()+self.iqtree_settings.get_values())
		
	def spawn_treesearch_settings_window(self):
		settings_window=Toplevel()
		settings = TreesearchSettingsWindow(settings_window,self.treesearch_settings)
		self.master.wait_window(settings_window)
		# self.info_label.insert(END, self.get_time()+"Treesearch parameters are:\n")
		# self.info_label.insert(END, self.get_time()+self.treesearch_settings.get_values())
	
	def get_time(self):
		return "["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+"]\t"
	
	def add_alignment(self):
		filename = "no file name"
		filename = tkFileDialog.askopenfilename(initialdir = "~",title = "Select alignment")
		print filename
		if filename != "" and filename != "no file name":
			self.alignments.append(Alignment(self.alignment_scroll_frame, align_id="Alignment "+str(len(self.alignments)+1)+":  ", path = filename, number=len(self.alignments)+1))
			self.alignments[-1].grid(sticky=W)
			self.align_offset += 30
			self.alignment_scroll_frame.update()
			self.alignment_info_label.config(text="Alignments: %s Alignment(s) loaded" % str(len(self.alignments)))
		
	"""	
	def open_partition(self):
		self.filename_partition = tkFileDialog.askopenfilename(initialdir = "~",title = "Select alignment")
		print self.filename_partition
		f = open(self.filename_partition,"r")
		partition = ""
		for line in f.readlines():
			partition += line
		self.partition_view.delete("1.0",END)
		self.partition_view.insert(END, partition)
		f.close()
		self.model_partitions = []
		self.is_models_set=False # will maybe also reset partitions if cancel is clicked!
	"""
		
	def create_partition(self):
		alignment_names = [element.alignment_id.strip(": ") for element in self.alignments]
		if len(alignment_names) == 0: # in case there is no alignment loaded, return. probably this needs a message box
			print "no alignments loaded"
			tkMessageBox.showerror("Error", "First specify at least one alignment.")
			return
		print alignment_names
		self.align_partitions.append(Partition(self.partitions_set_frame, part_id="Partition "+str(len(self.align_partitions)+1)+"  ", alignments = alignment_names, number = len(self.align_partitions)+1))
		self.align_partitions[-1].grid()
		self.partitions_set_frame.update()
		self.partition_info_label.config(text="Partitions: %s Partitions specified" % str(len(self.align_partitions)))
		"""
		if len(self.align_partitions) > len(self.model_partitions):
			self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Partition "+str(len(self.model_partitions)+1)))
			self.model_partitions[-1].grid(sticky=W)
			self.part_offset+=30
		self.manual_model_frame.update()
		self.model_frame_down.grid_forget()
		"""
		print "Partition created"
	
	def reset_partitions(self):
		for i in range(0, len(self.align_partitions)): # partitions
			self.align_partitions[i].grid_forget()
		self.align_partitions[:] = []
		self.partitions_set_frame.update()
		self.partition_info_label.config(text="Partitions: unpartitioned")
		"""
		for i in range(0, len(self.model_partitions)): # models
			self.model_partitions[i].grid_forget()
		self.part_offset=0
		self.model_partitions[:] = []
		self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Partition 1"))
		self.model_partitions[-1].grid(sticky=W)
		self.part_offset+=30
		self.manual_model_frame.update()
		"""
		
	def delete_partition(self):
		if len(self.align_partitions) > 0:
			self.align_partitions[-1].grid_forget()
			self.align_partitions = self.align_partitions[:-1]
		"""if len(self.model_partitions) > 1:
			self.model_partitions[-1].grid_forget()
			self.model_partitions = self.model_partitions[:-1]
			self.part_offset-=30
		self.manual_model_frame.update()
		"""
		self.partition_info_label.config(text="Partitions: %s Partitions specified" % str(len(self.align_partitions)))
		self.partitions_set_frame.update()
		# self.info_label.insert(END, self.get_time()+"Partition deleted\n")
		
	def create_models(self): # function will create model instances according to the specified alignment and partition options
		if len(self.alignments) == 1:
			print "create_model: single alignment"
			if self.choice_part_option == 1: #no partitioning
				print "create_model: no partition"
				self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Alignment 1"))
				self.model_partitions[-1].grid(sticky=W)
				self.part_offset+=30
				self.manual_model_frame.update()
			elif self.choice_part_option == 2: #partitions
				if len(self.align_partitions) == 0:
					tkMessageBox.showerror("Error", "Specify at least one partition per alignment first.")
					return
				else:
					print "create_model: multiple partitions"
					for i in range(0, len(self.align_partitions)):
						self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Partition %s" % str(i+1)))
						self.model_partitions[-1].grid(sticky=W)
						self.part_offset+=30
						self.manual_model_frame.update()			
		elif len(self.alignments) > 1: #multiple alignments
			print "create_model: multiple alignments"
			if self.choice_part_option == 1: #no partitioning
				print "create_model: no partitions"
				for i in range(0, len(self.alignments)):
					self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Alignment %s" % str(i+1)))
					self.model_partitions[-1].grid(sticky=W)
					self.part_offset+=30
					self.manual_model_frame.update()
			elif self.choice_part_option == 2: #partitions
				if len(self.align_partitions) == 0 or (len(self.align_partitions) < len(self.alignments)):
					tkMessageBox.showerror("Error", "Specify at least one partition per alignment first.")
					return
				else:
					print "create_model: multiple partitions"
					for i in range(0, len(self.align_partitions)):
						self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Partition %s" % str(i+1)))
						self.model_partitions[-1].grid(sticky=W)
						self.part_offset+=30
						self.manual_model_frame.update()
		self.model_info_label.config(text="Models: %s Models specified" % str(len(self.model_partitions)))
						
	def reset_models(self):
		print "reset_models: Removing " +str(len(self.model_partitions))+" partitions"
		for i in range(0, len(self.model_partitions)):
			self.model_partitions[i].grid_forget()
		self.model_partitions[:] = []
		self.part_offset=0
		self.manual_model_frame.update()
					
			
		
	def get_partitions(self):
		return len(self.align_partitions)
		
	def get_additional_settings_for_run(self):
		add_cmd = ""
		print self.advanced_model_settings.get_command()
		add_cmd += self.iqtree_settings.get_command()
		add_cmd += self.advanced_bs_settings.get_command()
		add_cmd += self.treesearch_settings.get_command()
		return add_cmd
	
	def get_run_command_new(self):
		print "creating run command"
		print "Alignments: %d " % len(self.alignments)
		print "Partitions: %d " % len(self.align_partitions)
		print "Models: %d" % len(self.model_partitions)
		## create initial run command
		command = self.gui_settings.iqtree_path +" "
		## add number of threads
		command += "-nt %s " % str(self.nthreads)
		partition_command=""
		
		## select bootstrap option:
		if self.choice_bs_option == 2:
			try:
				int(self.entry_bs.get())
				command += "-b %s " % self.entry_bs.get()
			except:
				tkMessageBox.showerror("Error", "Not a valid number of bootstrap replicates.")
				return
				
		if self.choice_bs_option == 3:
			try:
				int(self.entry_bs.get())
				command += "-bb %s " % self.entry_bs.get()
			except:
				tkMessageBox.showerror("Error", "Not a valid number of bootstrap replicates.")
				return
		
		if len(self.alignments) == 0:
			print "no alignment"
			return 
		### if there is only a single alignment:
		elif len(self.alignments) == 1:
			print "single alignment"
			partition_command=""
			## add model parameters for single partition:
			if self.choice_part_option == 1:	
				# check for different model options
				if self.choice_model_option == 1:
					command += self.advanced_model_settings.get_command()
				if self.choice_model_option == 2:
					if "invalid" in self.model_partitions[0].get_model():
						tkMessageBox.showerror("Error", "Specified model for Partition 1 " + self.model_partitions[0].get_model())
					else:
						if ("CODON" in self.model_partitions[0].get_model()): #handly codon models differently
							command += "-st " + self.model_partitions[0].get_model()+" "
						else:
							command += "-m " + self.model_partitions[0].get_model()+" "
						print self.model_partitions[0].model.__dict__
			## add model parameters for multiple partition	
			if self.choice_part_option == 2:
		
				# check for different model options
				## if modeltest should be used
				if self.choice_model_option == 1:
					command += self.advanced_model_settings.get_command()

				## add parameters for multiple partition:
				## if there are multiple partitions and models			
				if self.choice_model_option == 2:
					partition_command="#NEXUS\nbegin sets;\n"
					## first get partition boundaries:
					for part in range(0,len(self.align_partitions)):
						partition_command += "charset part"+str(part+1) +"= "+str(self.align_partitions[part].get_start())+ "-"+str(self.align_partitions[part].get_end())+";\n"
				
					## second add models:
					model_string = "charpartition mine = "
					print "found partitions: %s" % len(self.model_partitions)
					for i in xrange(0, len(self.model_partitions)):
						model = self.model_partitions[i].get_model()
						print model
						if "invalid" in model:
							tkMessageBox.showerror("Error", "Specified model for Partition " + str(i+1))
							break
						else:
							model_string += model
							model_string +=":part%s," % str(i+1)
							#print self.model_partitions[i].model.__dict__
					model_string = model_string[:-1]
					model_string += ";\nend;\n"
					partition_command += model_string
					print partition_command
				if self.choice_model_option == 1 and len(self.align_partitions)>1:
					partition_command="#NEXUS\nbegin sets;\n"
					## first get partition boundaries:
					for part in range(0,len(self.align_partitions)):
						partition_command += "charset part"+str(part+1) +"= "+str(self.align_partitions[part].get_start())+ "-"+str(self.align_partitions[part].get_end())+";\n"
					partition_command += "end;\n"
			
			## add alignment (only if there is 1 alignment)
			if self.filename != "":
				command += "-s "
				command += self.alignments[0].alignment_path
			else:
				tkMessageBox.showerror("Error", "No alignment loaded")
				return
			if self.overwrite == 1:
				command += " -redo "	
				self.partition_command = partition_command

		### if there are multiple alignments
		elif len(self.alignments) > 1:
			print "multiple alignments"

			
			#### Baustelle hier!!
			### multiple alignments, no partitions, modeltest = models per alignment
			if len(self.align_partitions) == 0 and self.choice_model_option == 1:
				print "multiple alignments, no partitions, modeltest"
				command += self.advanced_model_settings.get_command() #first add model testing option to run command
				partition_command="#NEXUS\nbegin sets;\n"
				i = 1
				for alignment in self.alignments:
					partition_command += "charset part" + str(i) + "= "+alignment.alignment_path + ":*;\n"
					i += 1
				partition_command +="end;\n"
			
			### multiple alignments, multiple partitions, modeltest = models per alignment (modeltest)
			elif len(self.align_partitions) >= 1 and self.choice_model_option == 1:
				print "muliple alignments, multiple partitions, modeltest"
				command += self.advanced_model_settings.get_command() #first add model testing option to run command
				partition_command="#NEXUS\nbegin sets;\n"
				i = 1
				for partition in self.align_partitions:
					alignment = self.alignments[partition.get_which_alignment()-1]
					partition_command += "charset part" + str(i) + "="+alignment.alignment_path + ":" + " " + str(partition.get_start()) +"-" +str(partition.get_end()) +";\n"
					i += 1
				for alignment in self.alignments:
					if alignment.alignment_path not in partition_command:
						partition_command += "charset part" + str(i) + "="+alignment.alignment_path + ":" + " *;\n"
						i +=1 
				partition_command +="end;\n"	
				
			### multiple alignments, multiple partitions, models per partition
			elif len(self.align_partitions) >= 1 and self.choice_model_option == 2:
				print "muliple alignments, multiple partitions, models per partition"
				command += self.advanced_model_settings.get_command() #first add model testing option to run command
				partition_command="#NEXUS\nbegin sets;\n"
				i = 1
				for partition in self.align_partitions:
					alignment = self.alignments[partition.get_which_alignment()-1]
					partition_command += "charset part" + str(i) + "="+alignment.alignment_path + ":" + " " + str(partition.get_start()) +"-" +str(partition.get_end()) +";\n"
					i += 1
				for alignment in self.alignments:
					if alignment.alignment_path not in partition_command:
						partition_command += "charset part" + str(i) + "="+alignment.alignment_path + ":" + " *;\n"
						i +=1 
				## second add models:
				model_string = "charpartition mine = "
				print "found partitions: %s" % len(self.model_partitions)
				for i in xrange(0, len(self.model_partitions)):
					model = self.model_partitions[i].get_model()
					print model
					if "invalid" in model:
						tkMessageBox.showerror("Error", "Check model for Partition " + str(i+1))
						break
					else:
						model_string += model
						model_string +=":part%s," % str(i+1)
				partition_command += model_string.strip(",")
				partition_command +=";\nend;\n"
			
			#### to here all for multiple partitions
				
		### the stuff from here should be the same regardless of the other options
		## check for partition command and adjust
		if partition_command != "":
			file = open(self.gui_settings.wd+"/partitions.nex", "w")
			file.write(partition_command)
			file.close()
			if "(-spp)" in self.partition_model:
				command += "-spp "+self.gui_settings.wd+"/partitions.nex "
			elif "(-q)" in self.partition_model:
				command += "-q "+self.gui_settings.wd+"/partitions.nex "
			elif "(-sp)" in self.partition_model:
				command += "-sp "+self.gui_settings.wd+"/partitions.nex "
			else:
				command += "-spp "+self.gui_settings.wd+"/partitions.nex " #standard	
		
		## additional settings
		command += self.get_additional_settings_for_run()

		#repeat analysis
		if self.overwrite == 1:
			command += " -redo "	
		self.partition_command = partition_command
		
		## make sure the command looks good
		print partition_command
		print command
		# self.info_label.insert(END, self.get_time()+"iqtree command will be: "+command+"\n")
		
		if self.simulate_only == 0:
			self.spawn_iqtree_subprocess(command)		
		
	"""			
	def get_run_command(self):
		print "Run analysis"
		if not os.path.isfile(self.gui_settings.iqtree_path):
			tkMessageBox.showerror("Error", "IQtree executable not found.\n Is the specified path correct?")
			return
		command = self.gui_settings.iqtree_path +" "
		
		## get thread number 
		command += "-nt %s " % str(self.nthreads)
		
		## select bootstrap option:
		if self.choice_bs_option == 2:
			try:
				int(self.entry_bs.get())
				command += "-b %s " % self.entry_bs.get()
			except:
				tkMessageBox.showerror("Error", "Not a valid number of bootstrap replicates.")
				return
				
		if self.choice_bs_option == 3:
			try:
				int(self.entry_bs.get())
				command += "-bb %s " % self.entry_bs.get()
			except:
				tkMessageBox.showerror("Error", "Not a valid number of bootstrap replicates.")
				return
				
		partition_command=""
		## add model parameters for single partition:
		if self.choice_part_option == 1:	
			# check for different model options
			if self.choice_model_option == 1:
				command += self.advanced_model_settings.get_command()
			if self.choice_model_option == 2:
				if "invalid" in self.model_partitions[0].get_model():
					tkMessageBox.showerror("Error", "Specified model for Partition 1 " + self.model_partitions[0].get_model())
				else:
					if ("CODON" in self.model_partitions[0].get_model()): #handly codon models differently
						command += "-st " + self.model_partitions[0].get_model()+" "
					else:
						command += "-m " + self.model_partitions[0].get_model()+" "
					print self.model_partitions[0].model.__dict__
		
		## add model parameters for multiple partition	
		if self.choice_part_option == 2:
		
			# check for different model options
			## if modeltest should be used
			if self.choice_model_option == 1:
				command += self.advanced_model_settings.get_command()

			## add parameters for multiple partition:
			## if there are multiple partitions and models			
			if self.choice_model_option == 2:
				partition_command="#NEXUS\nbegin sets;\n"
				## first get partition boundaries:
				for part in range(0,len(self.align_partitions)):
					partition_command += "charset part"+str(part+1) +"= "+str(self.align_partitions[part].get_start())+ "-"+str(self.align_partitions[part].get_end())+";\n"
				
				## second add models:
				model_string = "charpartition mine = "
				print "found partitions: %s" % len(self.model_partitions)
				for i in xrange(0, len(self.model_partitions)):
					model = self.model_partitions[i].get_model()
					print model
					if "invalid" in model:
						tkMessageBox.showerror("Error", "Specified model for Partition " + str(i+1))
						break
					else:
						model_string += model
						model_string +=":part%s," % str(i+1)
						#print self.model_partitions[i].model.__dict__
				model_string = model_string[:-1]
				model_string += ";\nend;\n"
				partition_command += model_string
				print partition_command
			if self.choice_model_option == 1 and len(self.align_partitions)>1:
				partition_command="#NEXUS\nbegin sets;\n"
				## first get partition boundaries:
				for part in range(0,len(self.align_partitions)):
					partition_command += "charset part"+str(part+1) +"= "+str(self.align_partitions[part].get_start())+ "-"+str(self.align_partitions[part].get_end())+";\n"
				partition_command += "end;\n"
		
		## check for partition command and adjust
		if partition_command != "":
			file = open(self.gui_settings.wd+"/partitions.nex", "w")
			file.write(partition_command)
			file.close()
			if "(-spp)" in self.partition_model:
				command += "-spp "+self.gui_settings.wd+"/partitions.nex "
			elif "(-q)" in self.partition_model:
				command += "-q "+self.gui_settings.wd+"/partitions.nex "
			elif "(-sp)" in self.partition_model:
				command += "-sp "+self.gui_settings.wd+"/partitions.nex "
			else:
				command += "-spp "+self.gui_settings.wd+"/partitions.nex " #standard	
		
		## add alignment
		if self.filename != "":
			command += "-s "
			command += self.filename 
		else:
			tkMessageBox.showerror("Error", "No alignment loaded")
			return
		
		if self.overwrite == 1:
			command += " -redo "	
		self.partition_command = partition_command
		
		
		## additional settings
		command += self.get_additional_settings_for_run()
		
	
		## make sure the command looks good
		print partition_command
		print command
		# self.info_label.insert(END, self.get_time()+"iqtree command will be: "+command+"\n")
		
		if self.simulate_only == 0:
			self.spawn_iqtree_subprocess(command)
	"""
				
	def spawn_iqtree_subprocess(self, command):	
		iqtree_out_window=Toplevel(self.master)
		iqtree_out = IqtreeWindow(iqtree_out_window, self.gui_settings)
		iqtree_out.send_command(command)
		iqtree_out.spawn_process()
		
	
	def update_notebook(self, button):
		self.manual_model_frame.update()	
		
	def read_config_file(self):
		config = ConfigParser.ConfigParser()
		print "reading config file"
		print self.config_path
		try:
			config.read(self.config_path)
			self.gui_settings.iqtree_path = config.get('Settings', 'iqtree')
			#self.gui_settings.wd = config.get('Settings', 'wd')
		except:
			tkMessageBox.showerror("Error", "Config file error")
			return

	def __init__(self, top):
		os.chdir(self.gui_settings.wd) # this is needed for the bundled mac app
		_bgcolor = 'gray85'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = 'gray85' # X11 color: 'gray85'
		_ana1color = 'gray85' # X11 color: 'gray85' 
		_ana2color = 'gray85' # X11 color: 'gray85' 
		self.master = top
		top.geometry("1000x593")#+330+201")
		top.title("iqtreeGUI Alpha")
		top.resizable(width=False, height=False)
		top.grid_rowconfigure(0, weight=1)
		top.grid_columnconfigure(0, weight=1)
		#top.iconbitmap(resource_path("iqtreegui.ico"))
		
		if "Linux" in platform.system() or "Darwin" in platform.system():
			self.config_path=os.path.expanduser("~/.iqtree_config")
		if "Windows" in platform.system():
			self.config_path="iqtree_config.cfg"
		
		

#### BASIC NOTEBOOK #######
		self.notebook = ttk.Notebook(top)
		self.notebook.bind("<ButtonRelease-1>", self.update_notebook)
		
		if root.tk.call('tk', 'windowingsystem') == 'aqua': #change padding of notebook tabs if osx
			s=ttk.Style()
			s.configure("TNotebook.Tab", padding=(18, 8, 20, 0))
		
		#self.notebook.place(relx=0, rely=0, relheight=0.9, relwidth=1)
		self.notebook.grid(row=0, column=0,columnspan=10, rowspan=1, sticky=N+S+W+E)

		
		## threads selection
		self.Label3 = Label(top)
		#self.Label3.place(relx=0.15, rely=0.94, height=18, width=130)
		self.Label3.configure(text='''Number of threads:''')
		self.Label3.grid(row=1, column=4, sticky=W)
		
		threads = [str(i) for i in range(1, multiprocessing.cpu_count()+1)]
		threads = ["AUTO"] + threads
		var_thread = StringVar()
		var_thread.set(threads[0])
		
		def cbOption_threads(which):
			self.nthreads = which
			# self.info_label.insert(END, self.get_time()+"Number of threads is set to "+self.nthreads+"\n")
			print "Number of threads set to %s" % self.nthreads
		
		self.threads_select = OptionMenu(top, var_thread,  *threads, command=cbOption_threads)
		#self.threads_select.place(relx=0.31, rely=0.93, height=26, width=65)
		self.threads_select.grid(row=1, column=5, sticky=W)
		self.button_run = Button(top)
		#self.button_run.place(relx=0.01, rely=0.93, height=26, width=102)
		self.button_run.grid(row=1,column=0, sticky=W)
		#self.button_run.configure(activebackground="#d9d9d9")
		self.button_run.configure(text='''Run Analysis''', command=self.get_run_command_new)
		
		cb_overwritevar = IntVar()
		cb_overwritevar.set(1)
		
		def cb_overwrite():
			self.overwrite = cb_overwritevar.get()
			#print self.overwrite
			# self.info_label.insert(END, self.get_time()+"Overwrite analysis is set to "+str(self.overwrite)+"\n")
			
		self.overwrite_analysis = Checkbutton(top, text="Overwrite analysis (-redo)",variable=cb_overwritevar,command=cb_overwrite)
		self.overwrite_analysis.grid(row=1, column=1, sticky=W)
		
		cb_simulate_only_var = IntVar()
		cb_simulate_only_var.set(1)
		def cb_simulate_only():
			self.simulate_only = cb_simulate_only_var.get()
			# self.info_label.insert(END, self.get_time()+"Simulate only is set to "+str(self.simulate_only)+"\n")
			
		self.simulate_only_check = Checkbutton(top, text="Simulate (only display iqtree command)  ",variable=cb_simulate_only_var,command=cb_simulate_only)
		self.simulate_only_check.grid(row=1, column=2, sticky=W)
		
########INFO#########
		
		self.info_frame = Frame(self.notebook)
		#self.info_frame.grid_rowconfigure(1, weight=1)
		#self.info_frame.grid_columnconfigure(1, weight=1)
		#self.info_label = ScrolledText(self.info_frame)
		#self.info_label.pack(fill=BOTH, expand=1)
		
		#print resource_path("icon/iqtreegui.gif")
		#print os.path.exists(os.path.join(sys.path[0],"iqtreegui.py"))
		#print os.path.dirname(os.path.realpath(__file__))
		#print sys.path[0]
		print resource_path("/icon/iqtreegui.gif")
		self.img=PhotoImage(file=resource_path("/icon/iqtreegui.gif"))
		#print self.img
		self.info_frame.columnconfigure(0, minsize=250)
		self.info_frame.rowconfigure(0, minsize=50)
		
		#self.canvas = Canvas(self.info_frame, width = 300, height = 200, bg = 'yellow')
		#self.canvas.grid(row =1,column=1)
		#self.canvas.create_image(1, 1, image = self.img)
		
		self.logo_cv = Label(self.info_frame, image=self.img)
		self.logo_cv.image = self.img
		self.logo_cv.grid(row=1, column=1, rowspan=5, sticky=W)
		
		#welcome_message = "_       __                 ________  ______\n (_)___ _/ /_________  ___  / ____/ / / /  _/\n/ / __ `/ __/ ___/ _ \/ _ \/ / __/ / / // /  \n/ / /_/ / /_/ /  /  __/  __/ /_/ / /_/ // /   \n/_/\__, /\__/_/   \___/\___/\____/\____/___/   \n/_/"
			         
		message = "iqtreeGUI - A graphical user interface for IQ-TREE.\n\nhttp://github.com/reslp/iqtree\n\nVersion %s \n\n" % self.gui_settings.version
		self.label = Label(self.info_frame, text=message)
		self.label.configure(font="Helvetica 14 bold")
		self.label.config(justify=LEFT)
		self.label.grid(row=1, column=2, sticky=NW)
		
		self.info_frame.rowconfigure(6, minsize=20)
		
		self.overview_label = Label(self.info_frame, text = "Overview of current analysis:")
		self.overview_label.configure(font="Helvetica 14 bold")
		self.overview_label.grid(row=7,column=1, columnspan=3, sticky=W)
		
		self.alignment_info_label = Label(self.info_frame, text="Alignments: no alignment loaded")
		self.alignment_info_label.config(justify=LEFT)
		self.alignment_info_label.grid(row=9, column=1, columnspan=3, sticky=W)
		
		self.partition_info_label = Label(self.info_frame, text="Partitions: unpartitioned")
		self.partition_info_label.config(justify=LEFT)
		self.partition_info_label.grid(row=10, column=1, columnspan=3, sticky=W)
		
		self.model_info_label = Label(self.info_frame, text="Models: automated model selection")
		self.model_info_label.config(justify=LEFT)
		self.model_info_label.grid(row=11, column=1, columnspan=3, sticky=W)
		
		self.bootstrap_info_label = Label(self.info_frame, text="Bootstrap: no bootstraping")
		self.bootstrap_info_label.config(justify=LEFT)
		self.bootstrap_info_label.grid(row=12, column=1, columnspan=3, sticky=W)		
		
		
		
		#self.info_label.tag_configure("center", justify='center')
		# self.info_label.insert(END, welcome_message)
		
		# load settings file, create if it does not exist
		#tkMessageBox.showerror("Error", resource_path('/config.txt'))
		print self.config_path
		if not os.path.isfile(self.config_path): #check if config file exists
			config = ConfigParser.ConfigParser()
			configfile = open(self.config_path, 'wb')
			config.add_section('Settings')
			config.set('Settings', 'iqtree', self.gui_settings.iqtree_path)
			config.set('Settings', 'version', self.gui_settings.version)
			#config.set('Settings', 'wd', self.gui_settings.wd)
			config.write(configfile)
			configfile.close()
			print "config file not found"
			## self.info_label.insert(END, self.get_time()+"No config file found. I created a new one...\n")
		else:
			self.read_config_file()
			
		
		# self.info_label.insert(END, "Version Alpha " +self.gui_settings.version+"\n\n")
		# self.info_label.insert(END, self.get_time()+"Configuration file loaded\n")
		# self.info_label.insert(END, self.get_time()+"Specified path to iqtree command is: "+ self.gui_settings.iqtree_path +"\n")
		# self.info_label.insert(END, self.get_time()+"Start by loading an alignment...\n")
		
		self.notebook.add(self.info_frame, text="Info")



###ALIGNMENT########
		## create frame for scrollbars and alignment view
		self.alignment_frame = Frame(self.notebook)
		self.alignment_frame.grid(sticky=N+W+S+E)
		
		self.alignment_frame.rowconfigure(0, minsize=30)
		self.alignment_frame.columnconfigure(0, minsize=30)
		self.alignment_frame.grid_rowconfigure(4,weight=1)
		self.alignment_frame.grid_columnconfigure(1,weight=1)

		
		self.description = tk.Label(self.alignment_frame,text="Specify alignment files (FASTA, PHYLIP, NEXUS) here: ", justify=tk.LEFT)
		self.description.configure(font="Helvetica 14 bold")
		self.description.grid(row=1,column=1, sticky=W)
		

		
		## create alignment button
		self.load_alignment_button = Button(self.alignment_frame)
		self.load_alignment_button.grid(row=2,column=1,sticky=W)
		self.load_alignment_button.configure(text="Add alignment", command=self.add_alignment)
		
		
		self.alignment_frame_container = Frame(self.alignment_frame)
		self.alignment_frame_container.grid(row=4, column=1, columnspan=10, sticky=N+S+W+E)
		self.alignment_scroll_frame = ScrollableFrame(self.alignment_frame_container)
		
		
		
		#self.alignment_test_var = IntVar()
		#self.alignment_test_var.set(0)
		
		#self.test_alignment = tk.Checkbutton(self.alignment_frame, text="Basic alignment check", variable=self.alignment_test_var)
		#self.test_alignment.grid(row=3,column=1, sticky=W)
		
		#self.alingnment_info_label = Label(self.alignment_frame)
		#self.alingnment_info_label.grid(row=0,column=1,sticky=W)
		#self.alingnment_info_label.configure(text="No alignment loaded")
		
		#self.alignment_text_frame = Frame(self.alignment_frame)
		#self.alignment_text_frame.grid(sticky=N+S+W+E, columnspan=5)
		#self.alignment_text_frame.grid_rowconfigure(0, weight=1)
		#self.alignment_text_frame.grid_columnconfigure(0, weight=1)
		#self.alignment_text_frame.configure(relief=GROOVE, borderwidth=1)
		
		# create scrollbars and attach to grid
		#self.xscroll = Scrollbar(self.alignment_text_frame, orient=HORIZONTAL)
		#self.xscroll.grid(row=1,column=0, sticky=E+W)		
		#self.yscroll = Scrollbar(self.alignment_text_frame, orient=VERTICAL)
		#self.yscroll.grid(row=0,column=1, sticky=N+S)
		
		# create alignment view and attach to grid
		#self.alignment_view = Text(self.alignment_text_frame, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
		#self.alignment_view.configure(background="white")
		#self.alignment_view.configure(font=("TkTextFont", 11))
		#self.alignment_view.configure(selectbackground="#c4c4c4")
		#self.alignment_view.configure(width=90, bd=5)
		#self.alignment_view.configure(wrap=NONE)
		#self.alignment_view.insert(END, "No alignment loaded")
		#self.alignment_view.grid(row=0,column=0, sticky=N+S+W+E)
		
		# connect scrolling functionality
		#self.yscroll.config(command=self.alignment_view.yview)
		#self.xscroll.config(command=self.alignment_view.xview)
		
		# attach frame to notebook
		
		
		self.notebook.add(self.alignment_frame, text="Alignment")
			

###Partitioning########			
		## partitioning frame
		self.partition_option_frame = Frame(self.notebook) #original frame
		self.partition_option_frame.grid(sticky=N+S+W+E)
		self.partition_option_frame.configure(relief=GROOVE)
		self.partition_option_frame.columnconfigure(0, minsize=30)
		self.partition_option_frame.rowconfigure(0, minsize=30)
		
		
		self.description_part = Label(self.partition_option_frame,text="Specify partitions: ", justify=LEFT)
		self.description_part.configure(font="Helvetica 14 bold")
		self.description_part.grid(row=1,column=1, sticky=W)

		
		self.partition_layer = Label(self.partition_option_frame)
		self.partition_layer.grid(row=2,column=1,rowspan=20, columnspan=20, sticky=N+S+W+E)
		
		
		self.part_set_frame_container = Frame(self.partition_option_frame)
		self.part_set_frame_container.grid(row=4, column=2, columnspan=5, sticky=N+W+S+E)
		
		self.partitions_set_frame = ScrollableFrame(self.part_set_frame_container)
		
		self.button_create_part = Button(self.partition_option_frame)
		self.button_create_part.grid(row=3, column=2, sticky=N)
		self.button_create_part.configure(activebackground="#d9d9d9")
		self.button_create_part.configure(text="Create partition", command=self.create_partition)
		
		self.button_delete_part = Button(self.partition_option_frame)
		self.button_delete_part.grid(row=3,column=3, sticky=N)
		self.button_delete_part.configure(activebackground="#d9d9d9")
		self.button_delete_part.configure(text="Delete partition", command=self.delete_partition)
		
		#initial position hidden
		self.part_set_frame_container.lower(self.partition_layer)
		self.button_create_part.lower(self.partition_layer)
		self.button_delete_part.lower(self.partition_layer)
		
		
		partition_options = [("single partition",1),("multiple partitions",2)]
		
		self.part_var=IntVar()
		self.part_var.set(1)
	
		self.small_part_subframe = Frame(self.partition_option_frame)
		self.small_part_subframe.grid(row=2,column=1)
		
		
		def ShowChoice_part():
			self.choice_part_option=self.part_var.get()
			# self.info_label.insert(END, self.get_time()+"Partitioning changed to: "+partition_options[self.choice_part_option-1][0]+"\n")
			if self.part_var.get() == 1:
				self.part_set_frame_container.lower(self.partition_layer)
				self.button_create_part.lower(self.partition_layer)
				self.button_delete_part.lower(self.partition_layer)
				self.which_partition_model.lower(self.partition_layer)
				self.reset_partitions()	
			if self.part_var.get() == 2:
				self.part_set_frame_container.lift(self.partition_layer)
				self.button_create_part.lift(self.partition_layer)
				self.button_delete_part.lift(self.partition_layer)
				self.which_partition_model.lift(self.partition_layer)
			print(self.part_var.get())
		
		for option, val in partition_options:
			Radiobutton(self.small_part_subframe, 
				  text=option,
				  padx = 10,
				  pady = 10,
				  variable=self.part_var,
				  justify=LEFT,
				  command=ShowChoice_part,
				  value=val).grid(column=0, sticky=W, rowspan=3)
		
		partition_models = ["choose partition model", "same branch lengths (-q)", "own rates (-spp)", "own branchlengths (-sp)"]

		self.part_model_var = StringVar()
		self.part_model_var.set(partition_models[0])
		
		def cbOption(which):
			self.partition_model = which
			# self.info_label.insert(END, self.get_time()+"Partitioning branch model changed to: "+self.partition_model+"\n")
			print which
			print self.partition_model
			
		self.which_partition_model = OptionMenu(self.partition_option_frame, self.part_model_var,  *partition_models, command=cbOption)
		self.which_partition_model.grid(row=3,column=4, sticky=N)
		self.which_partition_model.lower(self.partition_layer)
	
		
		self.notebook.add(self.partition_option_frame, text="Partitioning")


		
			
###Evolutionary Model######
		self.model_frame = Frame(self.notebook)
		self.model_frame.grid(sticky=N+S+W+E)
		
		self.model_frame.grid_columnconfigure(1,weight=1)
		self.model_frame.grid_rowconfigure(3,weight=1)
		self.model_frame_top = Frame(self.model_frame)
		self.model_frame.columnconfigure(0, minsize=30)
		self.model_frame.rowconfigure(0, minsize=30)
		
		self.description_model = Label(self.model_frame_top,text="Specify models: ", justify=LEFT)
		self.description_model.configure(font="Helvetica 14 bold")
		self.description_model.grid(row=1,column=1, sticky=W)

		self.model_frame_top.grid(row=1, column=1, columnspan=20, sticky=N+S+W+E)
		model_options = [("automatic model selection",1), ("manual model specification",2)]
	   
	   	self.v_model_option=IntVar()
		self.v_model_option.set(1)
	   
		def ShowChoice_model_option(): 
			if self.v_model_option.get() == 1: #make different options visible
				self.model_frame_down.grid_forget()
				self.auto_model_select.grid(row=2,column=2, sticky=N+W)
				self.reset_models()
				self.model_info_label.config(text="Models: automated model selection")
			if self.v_model_option.get() == 2:
				self.model_frame_down.grid(row=3, column=1, sticky=N+S+W+E)
				self.auto_model_select.grid_forget()
				self.create_models()
			else:
				print "else"
			print "Model changed:"
			self.choice_model_option=self.v_model_option.get()
			# self.info_label.insert(END, self.get_time()+"Model settings changed to: "+model_options[self.choice_model_option-1][0]+"\n")
			print(self.v_model_option.get())
		
		self.small_model_subframe = Frame(self.model_frame_top)
		self.small_model_subframe.grid(row=2, column=1)
		
		for option, val in model_options:
			Radiobutton(self.small_model_subframe, 
				  text=option, padx = 10, pady = 10,
				  variable=self.v_model_option,
				  command=ShowChoice_model_option,
				  value=val).grid(column=1,sticky=W)
		self.auto_model_select = Label(self.model_frame_top, text="Uses automatic model selection and tree building (-m MFP) by default.\nSee Advanced Options -> Automatic model selection to change that.", justify=LEFT)
		self.auto_model_select.configure(foreground="red")
		self.auto_model_select.grid(row=2,column=2, sticky=N+W)
	
		self.model_frame_down = Frame(self.model_frame)
		self.model_frame_down.grid(row=3, column=1, sticky=N+W+E+S)
		
		self.manual_model_frame = ScrollableFrame(self.model_frame_down)
		self.manual_model_frame.grid_forget()
		
		self.notebook.add(self.model_frame, text="Model")
		#self.notebook.tab(3, state="hidden")

		"""
		# create initial model(s)
		if len(self.alignments) == 1:
			self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Alignment %d" % i))
			self.model_partitions[-1].grid(sticky=W)
			self.part_offset+=30
		elif len(self.alignments) > 1:
			if self.choice_part_option == 1:
				for i in xrange(0,len(self.alignments)):
					self.model_partitions.append(ModelSelection(self.manual_model_frame, part_id="   Alignment %d" % i))
					self.model_partitions[-1].grid(sticky=W)
					self.part_offset+=30
		#self.manual_model_frame.update()
		self.model_frame_down.grid_forget()
		"""
			

###BOOTSTRAP########		
		self.bootstrap_frame = Frame(self.notebook)
		#self.bootstrap_frame.grid(sticky=N+S+W+E)
		self.bootstrap_frame.columnconfigure(0, minsize=30)
		self.bootstrap_frame.rowconfigure(0, minsize=30)
		self.description_bs = Label(self.bootstrap_frame,text="Specify resampling: ", justify=LEFT)
		self.description_bs.configure(font="Helvetica 14 bold")
		self.description_bs.grid(row=1,column=1, sticky=W)
		bootstrap_options = [("no bootstrapping",1), ("nonparametric bootstrap (-b)",2), ("ultrafast approximation (-bb)",3)]
	   
	   	self.v=IntVar()
		self.v.set(1)
	   
		def ShowChoice():
			self.choice_bs_option=self.v.get()
			self.bootstrap_info_label.config(text="Bootstrap: "+ bootstrap_options[self.v.get()-1][0])
			# self.info_label.insert(END, self.get_time()+"Bootstrapping changed to: "+bootstrap_options[self.choice_bs_option-1][0]+"\n")
			print(self.v.get())
		
		self.small_bs_subframe = Frame(self.bootstrap_frame)
		self.small_bs_subframe.grid(sticky=W, row=2, column=1)
		
		for option, val in bootstrap_options:
			Radiobutton(self.small_bs_subframe, 
				  text=option, padx = 10, pady = 10,
				  variable=self.v,command=ShowChoice, value=val).grid(sticky=W)
		
		#self.bootstrap_frame.rowconfigure(2,minsize=100)
		
		## bootstrap entry
		self.Label1 = Label(self.bootstrap_frame, text="Number of bootstraps:")
		self.Label1.grid(row=4, column=1, sticky=W)
		
		self.entry_bs = Entry(self.bootstrap_frame)
		self.entry_bs.grid(row=4, column=2, sticky=W)
		self.entry_bs.insert(END, self.nbootstrap)
		
		self.notebook.add(self.bootstrap_frame, text="Bootstrap")

###### Top Menu
		
		self.menubar = Menu(top)
		self.file_menu = Menu(self.menubar, tearoff=0)
		self.file_menu.add_command(label="About", command=self.about_message)
		self.file_menu.add_command(label="Load Analysis", command=self.load_analysis)
		self.file_menu.add_command(label="Save Analysis", command=self.save_analysis)	
		self.file_menu.add_command(label="Settings", command=self.spawn_settings_window)
		self.file_menu.add_command(label="Quit", command=top.quit)
		
		
		self.menubar.add_cascade(label="iqtreeGUI", menu=self.file_menu)
		
		self.advanced_menu = Menu(self.menubar, tearoff=0)
		self.advanced_menu.add_command(label="IQ-TREE Settings", command=self.spawn_iqtree_settings_window)
		self.advanced_menu.add_command(label="Automatic Model Selection", command=self.spawn_model_selection_window)
		self.advanced_menu.add_command(label="Tree search", command=self.spawn_treesearch_settings_window)
		self.advanced_menu.add_command(label="Bootstrapping", command=self.spawn_advanced_bootstrap_window)
		self.menubar.add_cascade(label="Advanced options", menu=self.advanced_menu)
		
		self.special_menu = Menu(self.menubar, tearoff=0)
		self.special_menu.add_command(label="Create Consensus tree", command=self.spawn_consensus_tree_window)
		self.special_menu.add_command(label="Likelihood mapping", command=self.not_yet)
		self.special_menu.add_command(label="Ancestral Seq Reconstruction", command=self.not_yet)
		self.special_menu.add_command(label="Topology Tests", command=self.not_yet)
		self.special_menu.add_command(label="Robinson-Foulds", command=self.spawn_robionsonfoulds_window)
		self.special_menu.add_command(label="Generate random trees", command=self.spawn_random_tree_window)
		self.menubar.add_cascade(label="Special Applications", menu=self.special_menu)
		
		top.config(menu=self.menubar)



if __name__ == '__main__':
	root = Tk()
	top = iqtree_GUI(root)
	root.mainloop()
	#vp_start_gui()