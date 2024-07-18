import numpy as np
import pandas as pd 
from statsmodels.stats.multitest import multipletests as sm
import sys 
import sciluigi as sl
import logging
import os
from multiprocessing import Pool
from src.utils.filesystem import create_path_if_not_exists
from src.config.Config import Config


# Init logging
log = logging.getLogger('sciluigi-interface')

class SaveInterestSetsTask(sl.Task):
	"""
	Save interest gene sets to pass into WebGestalt. 
	Note: save both regional and interregional sets.
	"""

	group = sl.Parameter()
	phens = sl.Parameter()
	ptype = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_save_interest_sets(self):
		# Output target for interest gene sets
		return sl.TargetInfo(self, f'{self.basepath}/{Config.WEBG_INTEREST_SETS_OUTPUT_PATH}'.replace('GROUP_NAME', self.group))
		

	def requires(self):
		pass

	def run(self):
		group = self.group
		phens = self.phens
		ptype = self.ptype

		## regs 
		regs = Config.WEBG_REGS

		## paths
		twas_path = f'{Config.WEBG_TWAS_PATH}'.replace('GROUP_NAME', group).replace('PHENS', phens)
		itwa_path = f'{Config.WEBG_ITWA_PATH}'.replace('GROUP_NAME', group).replace('PHENS', phens)


		outs_path = str(self.out_save_interest_sets().path)
		create_path_if_not_exists(outs_path)

		## regional loop 
		if ptype == 'BON': alg = 'bonferroni'
		else: alg = 'fdr_bh'

		for reg in regs: 
			tfile = f'{twas_path}/{reg}.txt'
			tdata = pd.read_table(tfile, usecols=['gene', 'pvalue'])
			
			fkeep = sm(tdata['pvalue'], method=alg, alpha=0.05)[0]
			genes = tdata['gene'][fkeep]

			ofile = f'{outs_path}/{ptype}_{phens}_{reg}.txt'
			genes.to_csv(ofile, index=False, header=False)

		################################################################################

		## interregional loop (incl. regional)
		glist = {reg: [] for reg in regs} 
		rlist = [(gr, pr) for gr in regs for pr in regs]

		for (gr, pr) in rlist: 

			if gr == pr: tfile = f'{twas_path}/{gr}.txt'
			else: tfile = f'{itwa_path}/grex_{gr}_phen_{pr}.txt'

			tdata = pd.read_table(tfile, usecols=['gene', 'pvalue'])
			
			fkeep = sm(tdata['pvalue'], method=alg, alpha=0.05)[0]
			genes = tdata['gene'][fkeep].values
		
			glist[pr] = np.union1d(glist[pr], genes)

		for reg, genes in glist.items(): 
			ofile = f'{outs_path}/{ptype}_{phens}_interreg_{reg}.txt'
			print(f'{outs_path}/{ptype}_{phens}_interreg_{reg}.txt')
			with open(ofile, 'w') as f: 
				lines = '\n'.join(genes) + '\n'
				f.writelines(lines)
			
		self.done = True

	def complete(self):
		return self.done
	

if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		phens = sl.Parameter()
		ptype = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			# save_interest_sets_task = SaveInterestSetsTask(group=self.group, phens=self.phens, ptype=self.ptype)
			save_interest_sets_task = self.new_task('save_interest_sets_task', SaveInterestSetsTask, group=self.group, phens=self.phens, ptype=self.ptype, basepath=self.basepath)
			return save_interest_sets_task
		
	sl.run_local(main_task_cls=Workflow)