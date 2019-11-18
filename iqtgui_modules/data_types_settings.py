#!/usr/bin/env python
#written by Philipp Resl
#this are the classes for different config options
from os.path import expanduser

class IQtreeGUIConfig:
	def __init__(self):
		self.wd = expanduser("~")
		self.version = "18112019"
		self.iqtree_path = "iqtree"
		self.analysisname = "analysis"

class Model:
	def __init__(self):
		self.data_type = "Data Type"
		self.model_type = "Model Type"
		self.model = "Model"
		self.base_freq = "Freq"
		self.base_fre_fixed_scheme = "Enter Scheme"
		self.li_model_prefix = "Prefix"
		self.codon_subst_rate = "Subst Rate"
		self.aa_mixture_option = "Mix.Opt."
		self.user_scheme = "Enter Scheme"
		self.rate_hetero = "Rate Heterog."
					
class BootstrapConfig:
	def __init__(self):
		self.bcor = 0.99
		self.beps = 0.5
		self.bnni = 0
		self.bsam = "None" #not yet implemented
		self.nm = 1000
		self.nstep = 100
		self.wbt = 0
		self.wbtl = 0

	def get_command(self):
		cmd = ""
		if self.bcor != 0.99:
			cmd += "-bcor %f " % self.bcor
		if self.beps != 0.5:
			cmd += "-beps %f " % self.beps
		if self.bnni == 1:
			cmd += "-bnni "
		if self.nm != 1000:
			cmd += "-nm %d " % self.nm
		if self.nstep != 100:
			cmd += "-nstep %d " % self.nstep
		if self.wbt == 1:
			cmd += "-wbt "
		if self.wbtl == 1:
			cmd += "-wbtl "
		return cmd
		
class AutomaticModelSelectionSettings:
	def __init__(self):
		self.testonly = 0
		self.test = 0
		self.mf = 0
		self.mfp = 1
		self.lm_type = 0
		self.merge = 0
		self.mset = 0
		self.msub = 0
		self.cmin = 2
		self.cmax = 10
		self.merit = 0
		self.mtree = 0
		self.mredo = 0
	
	def get_command(self):
		cmd = ""
		if self.merge == 1:
			if self.testonly == 1:
				cmd += "-m TESTMERGEONLY"
			if self.test == 1:
				cmd += "-m TESTMERGE"
			if self.mf == 1:
				cmd += "-m MF+MERGE"
			if self.mfp == 1:
				cmd += "-m MFP+MERGE"
		if self.merge == 0:
			if self.testonly == 1:
				cmd += "-m TESTONLY"
			if self.test == 1:
				cmd += "-m TEST"
			if self.mf == 1:
				cmd += "-m MF"
			if self.mfp == 1:
				cmd += "-m MFP"
		if self.lm_type == 1:
			cmd += "+LM"
		if self.lm_type == 2:
			cmd += "+LMRY"
		if self.lm_type == 3:
			cmd += "+LMWS"
		if self.lm_type == 4:
			cmd += "+LMMK"
		if self.lm_type == 5:
			cmd += "+LMSS"

		if self.mset == 1:
			cmd += " -mset raxml"
		if self.mset == 2:
			cmd += " -mset phyml"
		if self.mset == 3:
			cmd += " -mset mrbayes"
		if self.msub == 1:
			cmd += " -msub mitochondrial"
		if self.msub == 2:
			cmd += " -msub chloroplast"
		if self.msub == 3:
			cmd += " -msub nuclear"
		if self.msub == 1:
			cmd += " -msub viral"
		if self.cmin != 2:
			cmd += " -cmin %d" % self.cmin
		if self.cmax != 10:
			cmd += " -cmax %d" % self.cmax
		if self.merit == 1:
			cmd += " -merit AIC"
		if self.merit == 2:
			cmd += " -merit AICc"
		if self.merit == 3:
			cmd += " -merit BIC"
		if self.mtree == 1:
			cmd += " -mtree"
		if self.mredo == 1:
			cmd += " -mredo"
		return cmd + " "
	
class IQtreeSettings:
	def __init__(self):
		self.t = 0
		self.starting_tree="None"
		self.te = 0
		self.bionj_tree = 0
		self.random_tree = 0
		self.o = "default"
		self.pre = "None"
		self.seed = "random"
		self.v = 0
		self.quiet=0
		self.keep_ident = 0
		self.save = 0
		self.mem = "default"
		
	def get_values(self):
		return "t=" + str(self.t)+" te="+str(self.te)+" bionj="+str(self.bionj_tree)+" random="+str(self.random_tree)+" o="+str(self.o)+" pre="+str(self.pre)+" seed=" +str(self.seed)+" v="+str(self.v)+" quiet="+str(self.quiet)+" ident="+str(self.keep_ident)+ " save="+str(self.save)+"\n"
	
	def get_dict(self):	
		return self.__dict__
		
	def get_command(self):
		cmd = ""
		if self.t == 1: # now this does not include the case where no starting tree is specified
			if self.te == 1:
				cmd += "-te %s " % self.starting_tree
			else:
				cmd += "-t %s " % self.starting_tree
		if self.bionj_tree == 1:
			cmd += "-t BIONJ "
		if self.random_tree == 1:
			cmd += "-t RANDOM "
		if self.o != "default":
			cmd += "-o %s " % self.o
		if self.pre != "None" and self.pre != "":
			cmd += "-pre %s " % self.pre
		if self.seed != "random":
			cmd += "-seed %s " % self.seed
		if self.v == 1:
			cmd += "-v "
		if self.quiet == 1:
			cmd += "-quiet "
		if self.keep_ident == 1:
			cmd += "-keep-ident "
		if self.save == 1:
			cmd += "-safe "
		return cmd
		
	def __eq__ (self, other):
		return self.__dict__ == other.__dict__
	def __ne__ (self, other):
		return self.__dict__ != other.__dict__
	
	
class TreeSearchSettings:
	def __init__(self):
		self.allnni = 0
		self.djc = 0
		self.fast = 0
		#self.constrained_tree = "" #not yet implemented
		self.ninit = 100
		self.n = 0
		self.ntop = 20
		self.nbest = 5
		self.nstop = 100
		self.pers = 0.5
		self.sprrad = 6
	
	def get_command(self):
		cmd = ""
		if self.allnni == 1:
			cmd += "-allnni "
		if self.djc == 1:
			cmd += "-djc "
		if self.fast == 1:
			cmd += "-fast "
		if self.ninit != 100:
			cmd += "-ninit %d " % self.ninit
		if self.n != 0:
			cmd += "-n %d " % self.n
		elif self.n == 0 and self.ntop != 20:
			cmd += "-ntop %d " % self.ntop
		if self.nbest != 5:
			cmd += "-nbest %d " % self.nbest
		if self.nstop != 100:
			cmd += "-nbest %d " % self.nstop
		if self.pers != 0.5:
			cmd += "-pers %f " % self.pers
		if self.sprrad != 6:
			cmd += "-sprrad %d " % self.sprrad
		return cmd		
	
	def get_values(self):
		return "allnni=" + str(self.allnni)+" djc="+str(self.djc)+" fast="+str(self.fast)+" constrained tree="+" ninit="+str(self.ninit)+" n="+str(self.n)+" ntop=" +str(self.ntop)+" nbest="+str(self.nbest)+" nstop="+str(self.nstop)+" pers="+str(self.pers)+ " sprrad="+str(self.sprrad)+"\n"