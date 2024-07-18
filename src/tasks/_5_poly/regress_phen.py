import numpy as np 
import pandas as pd 
from sklearn.linear_model import LinearRegression
import sys 
import logging
import sciluigi as sl
from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists
import os 


# Init logging
log = logging.getLogger('sciluigi-interface')


class RegressPhenTask(sl.Task):
	"""
	Regress covariates from phenotypes. 
	"""

	group = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_regress_phen(self):
		# Output target for regressed phenotypes
		return sl.TargetInfo(self, f'{self.basepath}/{Config.REGRESS_OUT_DIR}'.replace('GROUP_NAME', self.group))


	def requires(self):
		pass


	def get_residuals(self, x_covs, y_phen): 
		lr = LinearRegression().fit(x_covs, y_phen)
		y_pred = lr.predict(x_covs) 
		resids = y_phen - y_pred
		return resids 


	def run(self):
		
		covs_path = Config.POLY_COVS_PATH.replace('GROUP_NAME', self.group) ## covs
		phen_path = f'{Config.REGRESS_PHEN_PATH}'.replace('GROUP_NAME', self.group)    ## phen to be replaced below

		out_regress_phen = str(self.out_regress_phen().path)
		outs_path = f'{out_regress_phen}/{Config.REGRESS_OUTS_FILE}'.replace('GROUP_NAME', self.group)    ## phen to be replaced below

		create_path_if_not_exists(out_regress_phen)

		## read covariates 
		covs = pd.read_csv(covs_path, sep='\t')
		covs = covs.drop('eid', axis=1).values

		## phen loop 
		phens = Config.COMMON_PHENS
		for phen in phens: 
			# ADDON - @d-gopalkrishna - since we don't always have these phens. Let's check if they exist, if not then pass
			if not os.path.exists(phen_path.replace('PHEN_TYPE', phen)):
				continue

			## get original data, init new data
			pfile = phen_path.replace('PHEN_TYPE', phen)
			phen_old = pd.read_csv(pfile, sep='\t')
			phen_new = phen_old[['eid']].copy()

			## apply regression 
			regs = phen_old.columns[1:]
			for reg in regs: 
				reg_vals = phen_old[reg].values
				phen_new[reg] = self.get_residuals(covs, reg_vals)

			## write to file 
			ofile = outs_path.replace('PHEN_TYPE', phen).format(phen) 
			phen_new.to_csv(ofile, index=False, sep='\t')

		self.done = True

	
	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()
		group = sl.Parameter()

		def workflow(self):
			run_regress_phen = self.new_task('run_regress_phen', RegressPhenTask, group=self.group, basepath=self.basepath)
			return run_regress_phen
		
	# Run the workflow
	sl.run_local(main_task_cls=Workflow)

