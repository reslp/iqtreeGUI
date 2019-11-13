#! /usr/bin/env python
# tkinter Frame to allow complex model selection in iqtree gui
# written by Philipp Resl
import sys
from data_types_settings import *

try:
    from tkinter import *
except ImportError:
    from tkinter import *

try:
    import tkinter.ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

class ModelSelection(Frame):
	data_type = ""
	
	dna_model_type = ""
	dna_base_model = ""
	dna_base_freq = ""
	
	dna_li_model = ""
	dna_li_pre = ""
	
	dna_codon_model = ""
	dna_codon_subst = ""
	
	aa_model_type = ""
	aa_change_model = ""
	aa_freq = ""
	aa_mixture_model = ""
	
	morpho_model = ""
	
	rate_hetero = ""
	
	
	def load_model(self):
		self.data_type_v.set(self.model.data_type)
		if self.model.data_type == "DNA":
			self.dna_type_select.grid(column=2, row=0)
			self.dna_type_v.set(self.model.model_type)
			if self.model.model_type == "Base substitution rates":
				self.base_model_select.grid(row=0,column=3)
				self.base_freq_select.grid(row=0, column=4)
				self.rate_hetero_select.grid(row=0,column=7)
				self.v_model.set(self.model.model)
				self.v_base_freq.set(self.model.base_freq)
				self.rate_hetero_v.set(self.model.rate_hetero)	
			if self.model.model_type == "Lie Markov models":
				self.li_model_select.grid(row=0, column=4)
				self.li_model_prefix_select.grid(row=0, column=3)
				self.rate_hetero_select.grid(row=0,column=7)
				self.v_li_model_prefix.set(self.model.li_model_prefix)
				self.v_li_model.set(self.model.model)
				self.rate_hetero_v.set(self.model.rate_hetero)	
			if self.model.model_type == "Codon model":
				self.codon_subst_rate_select.grid(row=0, column=4)
				self.codon_model_select.grid(row=0, column=3)
				self.rate_hetero_select.grid(row=0,column=7)
				self.v_codon_model.set(self.model.model)
				self.v_codon_subst_rate.set(self.model.codon_subst_rate)
				self.rate_hetero_v.set(self.model.rate_hetero)		
			if self.model.model_type == "Specify manually":
				print() #not yet implemented
		if self.model.data_type == "AA":
			self.aa_type_select.grid(row=0,column=2)
			self.rate_hetero_select.grid(row=0,column=7)
			self.aa_type_v.set(self.model.model_type)
			self.rate_hetero_v.set(self.model.rate_hetero)	
			if self.model.model_type == "AA exchange rate matrices":
				self.aa_exchange_type_select.grid(row=0,column=3)
				self.aa_freq_select.grid(row=0, column=5)
				self.aa_exchange_type_v.set(self.model.model)
				self.v_aa_freq.set(self.model.base_freq)
				
			if self.model.model_type == "Mixture Models":
				self.aa_mixture_type_select.grid(row=0,column=3)
				self.aa_freq_select.grid(row=0, column=5)
				self.aa_mixture_type_v.set(self.model.aa_mixture_option)
				self.v_aa_freq.set(self.model.base_freq)
				
			if self.model.model_type == "User-defined":
				self.prot_user_scheme.grid(row=0,column=3)
				self.aa_freq_select.grid(row=0, column=5)
				self.prot_user_scheme.delete(0,END)
				self.prot_user_scheme.insert(END,self.model.user_scheme)
				self.v_aa_freq.set(self.model.base_freq)

			
	
	def create_widgets(self, part_id):
		self.partition_label = Label(self, text=part_id)
		self.partition_label.grid(column=0, sticky=W)
		self.partition_label.configure(font=("TkTextFont", 12, "bold"))

		data_type_options = ["DNA","AA"]#,"MORPH","SNP"]
		
		self.data_type_v=StringVar()
		self.data_type_v.set(self.model.data_type)
				
		def ShowChoice_data_type(which):
			if which == "DNA":
				self.dna_type_select.grid(column=2, row=0)
				self.aa_type_select.grid_forget()
				self.aa_exchange_type_select.grid_forget()
				self.aa_mixture_type_select.grid_forget()
				self.prot_user_scheme.grid_forget()
				self.aa_freq_select.grid_forget()
				self.fixed_aa_scheme.grid_forget()
				self.morph_type_select.grid_forget()
				self.rate_hetero_select.grid(row=0,column=7)
				self.rate_hetero_user_scheme.grid_forget()
				self.model.data_type = "DNA"
						
			if which == "AA":
				self.dna_type_select.grid_forget()
				self.li_model_select.grid_forget()
				self.li_model_prefix_select.grid_forget()
				self.base_model_select.grid_forget()
				self.base_freq_select.grid_forget()
				self.codon_subst_rate_select.grid_forget()
				self.codon_model_select.grid_forget()
				self.fixed_scheme.grid_forget()
				self.codon_subs_scheme.grid_forget()
				self.aa_type_select.grid(row=0,column=2)
				self.morph_type_select.grid_forget()
				self.rate_hetero_select.grid(row=0,column=7)
				self.rate_hetero_user_scheme.grid_forget()
				self.model.data_type = "AA"
				
			if which == "MORPH":
				self.dna_type_select.grid_forget()
				self.li_model_select.grid_forget()
				self.li_model_prefix_select.grid_forget()
				self.base_model_select.grid_forget()
				self.base_freq_select.grid_forget()
				self.codon_subst_rate_select.grid_forget()
				self.codon_model_select.grid_forget()
				self.fixed_scheme.grid_forget()
				self.codon_subs_scheme.grid_forget()
				self.aa_type_select.grid_forget()
				self.aa_exchange_type_select.grid_forget()
				self.aa_mixture_type_select.grid_forget()
				self.prot_user_scheme.grid_forget()
				self.aa_freq_select.grid_forget()
				self.fixed_aa_scheme.grid_forget()
				self.morph_type_select.grid(row=0,column=2)
				self.rate_hetero_select.grid(row=0,column=7)
				self.rate_hetero_user_scheme.grid_forget()
				self.model.data_type = "MORPH"

			if which == "SNP":	
				self.dna_type_select.grid_forget()
				self.li_model_select.grid_forget()
				self.li_model_prefix_select.grid_forget()
				self.base_model_select.grid_forget()
				self.base_freq_select.grid_forget()
				self.codon_subst_rate_select.grid_forget()
				self.codon_model_select.grid_forget()
				self.fixed_scheme.grid_forget()
				self.codon_subs_scheme.grid_forget()
				self.aa_type_select.grid_forget()
				self.aa_exchange_type_select.grid_forget()
				self.aa_mixture_type_select.grid_forget()
				self.prot_user_scheme.grid_forget()
				self.aa_freq_select.grid_forget()
				self.fixed_aa_scheme.grid_forget()
				self.morph_type_select.grid_forget()
				self.rate_hetero_user_scheme.grid_forget()
				self.model.data_type = "SNP"
				
			self.data_type = which
			
		self.data_type_select = OptionMenu(self, self.data_type_v,  *data_type_options, command=ShowChoice_data_type)
		self.data_type_select.grid(column=1, row=0)

		dna_model_options = ["Base substitution rates","Lie Markov models","Codon model"]#,"Specify manually"]

		self.dna_type_v=StringVar()
		self.dna_type_v.set(self.model.model_type)
		
		def ShowChoice_dna_type(which):
			if which == "Base substitution rates":
				self.base_model_select.grid(row=0,column=3)
				self.base_freq_select.grid(row=0, column=4)
				self.li_model_select.grid_forget()
				self.li_model_prefix_select.grid_forget()
				self.codon_subst_rate_select.grid_forget()
				self.codon_model_select.grid_forget()
				self.codon_subs_scheme.grid_forget()
			if which == "Lie Markov models":
				self.base_model_select.grid_forget()
				self.base_freq_select.grid_forget()
				self.li_model_select.grid(row=0, column=4)
				self.li_model_prefix_select.grid(row=0, column=3)
				self.codon_subst_rate_select.grid_forget()
				self.codon_model_select.grid_forget()
				self.codon_subs_scheme.grid_forget()	
			if which == "Codon model":
				self.base_model_select.grid_forget()
				self.base_freq_select.grid_forget()
				self.li_model_select.grid_forget()
				self.li_model_prefix_select.grid_forget()
				self.codon_subst_rate_select.grid(row=0, column=4)
				self.codon_model_select.grid(row=0, column=3)
			if which == "Specify manually":	
				self.base_model_select.grid_forget()
				self.base_freq_select.grid_forget()
				self.li_model_select.grid_forget()
				self.li_model_prefix_select.grid_forget()
				self.codon_subst_rate_select.grid_forget()
				self.codon_model_select.grid_forget()
				self.codon_subs_scheme.grid_forget()
			self.aa_freq_select.grid_forget()
			print("Model category: %s" % self.dna_type_v.get())
			self.dna_model_type=which
			self.model.model_type = which
		
		self.dna_type_select = OptionMenu(self, self.dna_type_v,  *dna_model_options, command=ShowChoice_dna_type)

		base_model_options = ["JC","F81","K80","HKY","TN","TNe","K81","K81u","TPM2","TPM2u","TPM3","TPM3u","TIM","TIMe","TIM2","TIM2e","TIM3","TIM3e","TVM","TVMe","SYM","GTR"]
		
		self.v_model=StringVar()
		self.v_model.set(self.model.model)
		
		def cbBaseModel(which): 
			self.dna_base_model = which	
			self.model.model = which	
			print(which)		
	
		self.base_model_select = OptionMenu(self, self.v_model,  *base_model_options, command=cbBaseModel)
		
		base_freq_options = ["+F", "+FQ", "+FO", "FIX"]
		
		self.v_base_freq=StringVar()
		self.v_base_freq.set(self.model.base_freq)
		
		def cbBaseFreq(which): 
			if which == "FIX":
				self.fixed_scheme.grid(row=0,column=5)
			else:
				self.fixed_scheme.grid_forget()
			self.model.base_freq = which
			self.dna_base_freq = which
			print(which)
	
		self.base_freq_select = OptionMenu(self, self.v_base_freq,  *base_freq_options, command=cbBaseFreq)
		self.fixed_scheme = Entry(self)
		self.fixed_scheme.insert(END, self.model.base_fre_fixed_scheme)
		
		
		li_model_prefix_options = ["RY", "WS", "MK", "None"]
		
		self.v_li_model_prefix = StringVar()
		self.v_li_model_prefix.set(self.model.li_model_prefix)
		
		def cbLiModel_prefix(which):
			self.dna_li_pre = which
			self.model.li_model_prefix = which
			print(which)
		
		self.li_model_prefix_select = OptionMenu(self, self.v_li_model_prefix,  *li_model_prefix_options, command=cbLiModel_prefix)
		
		
		li_model_options = ["1.1","2.2b","3.3a","3.3b","3.3c","3.4","4.4a","4.4b","4.5a","4.5b","5.6a","5.6b","5.7a","5.7b","5.7c","5.11a","5.11b","5.11c","5.16","6.6","6.7a","6.7b","6.8a","6.8b","6.17a","6.17b","8.8","8.10a","8.10b","8.16","8.17","8.18","9.20a","9.20b","10.12","10.34","12.12"]
		
		self.v_li_model = StringVar()
		self.v_li_model.set(self.model.model)
		
		def cbLiModel(which):
			self.dna_li_model = which
			self.model.model = which
			print(which)
		
		self.li_model_select = OptionMenu(self, self.v_li_model,  *li_model_options, command=cbLiModel)
		
		codon_model_options = ["CODON1","CODON2","CODON3","CODON4","CODON5","CODON6","CODON9","CODON10","CODON11","CODON12","CODON13","CODON14","CODON16","CODON21","CODON22","CODON23","CODON24","CODON25"]		
		
		self.v_codon_model = StringVar()
		self.v_codon_model.set(self.model.model)
		
		def cbCodonModel(which):
			self.dna_codon_model = which
			self.model.model = which
			print(which)
		
		self.codon_model_select = OptionMenu(self, self.v_codon_model,  *codon_model_options, command=cbCodonModel)
		
		codon_subst_rate_options = ["MG","MGK","MG1KTS or MGKAP2","MG1KTV or MGKAP3","MG2K or MGKAP4","GY","GY1KTS or GYKAP2","GY1KTV or GYKAP3","GY2K or GYKAP4","ECMK07 or KOSI07","ECMrest","ECMS05 or SCHN05", "Combined"]		
		
		self.v_codon_subst_rate = StringVar()
		self.v_codon_subst_rate.set(self.model.codon_subst_rate)
		
		def cbCodonRateOption(which):
			if which == "Combined":
				self.codon_subs_scheme.grid(row=0, column=5)
			else:
				self.codon_subs_scheme.grid_forget()
				self.dna_codon_subst=which
				self.model.codon_subst_rate = which
			print(which)
		
		self.codon_subst_rate_select = OptionMenu(self, self.v_codon_subst_rate,  *codon_subst_rate_options, command=cbCodonRateOption)
		self.codon_subs_scheme = Entry(self)
		self.codon_subs_scheme.insert(END, self.model.user_scheme)
		
		aa_model_options = ["AA exchange rate matrices","Mixture Models"]#,"User-defined"]

		self.aa_type_v=StringVar()
		self.aa_type_v.set(self.model.model_type)
		
		def ShowChoice_aa_type(which):
			self.aa_freq_select.grid(row=0, column=5)
			if which == aa_model_options[0]:
				self.aa_exchange_type_select.grid(row=0,column=3)
				self.aa_mixture_type_select.grid_forget()
				self.prot_user_scheme.grid_forget()
			if which == aa_model_options[1]:
				self.aa_exchange_type_select.grid_forget()
				self.aa_mixture_type_select.grid(row=0,column=3)
				self.prot_user_scheme.grid_forget()
			#if which == aa_model_options[2]:
			#	self.aa_exchange_type_select.grid_forget()
			#	self.aa_mixture_type_select.grid_forget()
			#	self.prot_user_scheme.grid(row=0,column=3)
			self.aa_model_type = self.aa_type_v.get()
			self.model.model_type = which
		
		self.aa_type_select = OptionMenu(self, self.aa_type_v,  *aa_model_options, command=ShowChoice_aa_type)
		
		
		aa_exchange_model_options = ["BLOSUM62","cpREV","Dayhoff","DCMut","FLU","HIVb","HIVw","JTT","JTTDCMut","LG","mtART","mtMAM","mtREV","mtZOA","mtMet","mtVer","mtInv","Poisson","PMB","rtREV","VT","WAG","GTR20"]

		self.aa_exchange_type_v=StringVar()
		self.aa_exchange_type_v.set(self.model.model)
		
		def ShowChoice_aa_exchange_type(which):
			self.aa_change_model = which
			self.model.model = which
			self.aa_mixture = ""
			print(which)
		
		self.aa_exchange_type_select = OptionMenu(self, self.aa_exchange_type_v,  *aa_exchange_model_options, command=ShowChoice_aa_exchange_type)
		
		
		aa_mixture_model_options = ["C10","C20","C30","C40","C50","C60","EX2","EX3","EHO","UL2","UL3","EX_EHO","LG4M","LG4X","CF4"]

		self.aa_mixture_type_v=StringVar()
		self.aa_mixture_type_v.set(self.model.aa_mixture_option)
		
		def ShowChoice_aa_mixture_type(which):
			self.aa_mixture_model = which
			self.model.aa_mixture_option = which
			self.aa_change_model = ""

		
		self.aa_mixture_type_select = OptionMenu(self, self.aa_mixture_type_v,  *aa_mixture_model_options, command=ShowChoice_aa_mixture_type)
		
		self.prot_user_scheme = Entry(self)
		self.prot_user_scheme.insert(END, self.model.user_scheme)
		
		
		aa_freq_options = ["+F", "+FQ", "+FO"]#, "FIX"]
		
		self.v_aa_freq=StringVar()
		self.v_aa_freq.set(self.model.base_freq)
		
		def cbAAFreq(which): 
			self.aa_freq = which
			self.model.base_freq = which
			if which == "FIX":
				self.fixed_aa_scheme.grid(row=0, column=6)
			else:
				self.fixed_aa_scheme.grid_forget()
			print(which)
	
		self.aa_freq_select = OptionMenu(self, self.v_aa_freq,  *aa_freq_options, command=cbAAFreq)

		self.fixed_aa_scheme = Entry(self)
		self.fixed_aa_scheme.insert(END, "Enter Scheme")

	
		morph_model_options = ["JC2","GTR2","MK","ORDERED"]

		morph_type_v=StringVar()
		morph_type_v.set("Model")
		
		def ShowChoice_morph_type(which):
			self.morpho_model = which
			print(which)
		self.morph_type_select = OptionMenu(self, morph_type_v,  *morph_model_options, command=ShowChoice_morph_type)
				
		rate_hetero_options = ["Rate Heterog.", "+I", "+G", "+I+G", "+R", "+I+R"]
		self.rate_hetero_v=StringVar()
		self.rate_hetero_v.set(self.model.rate_hetero)
		
		def ShowChoice_rate_hetero(which):
			if which == "FIX":
				self.rate_hetero_user_scheme.grid(row=0,column=8) #needs to be changed to lift when this is activated
			else:
				self.rate_hetero_user_scheme.grid_forget()
			self.model.rate_hetero=which	
			print(which)
		
		self.rate_hetero_select = OptionMenu(self, self.rate_hetero_v,  *rate_hetero_options, command=ShowChoice_rate_hetero)
		
		
		self.rate_hetero_user_scheme = Entry(self)
		self.rate_hetero_user_scheme.insert(END, self.model.user_scheme)
		
		


	def get_model(self): #this will be the function to return which model is used
		print("Returning model...")
		if self.model.rate_hetero=="Rate Heterog.":
			self.model.rate_hetero = ""
		if self.model.data_type == "DNA":
			if self.model.model_type == "Base substitution rates":
				model = self.model.model + self.model.base_freq + self.model.rate_hetero
				print("Model will be: %s" % model)
				return model
			if self.model.model_type == "Lie Markov models":
				if self.model.li_model_prefix == "Prefix" or self.model.li_model_prefix == "None":
					model = self.model.model + self.model.rate_hetero
				else: 
					model = self.model.li_model_prefix + self.model.model + self.model.rate_hetero
				print("Model will be: %s" % model)
				return model
			if self.model.model_type == "Codon model":
				model = self.model.model + "+" + self.model.codon_subst_rate + self.model.rate_hetero
				return model
			else:
				return "invalid DNA model"
		if self.model.data_type == "AA":
			if self.model.model_type == "AA exchange rate matrices":
				model = self.model.model + self.model.base_freq + self.model.rate_hetero
				return model
			if self.model.model_type == "Mixture Models":
				model = self.model.aa_mixture_option + self.model.base_freq + self.model.rate_hetero
				return model
		#add additional data types here
		else:
			return "invalid model"
		
		
	def __init__(self, master, part_id):
		self.model = Model()
		print(self.model.__dict__)
		
		Frame.__init__(self, master)
		self.master = master
		#self.pack()
		self.create_widgets(part_id)

		
	
