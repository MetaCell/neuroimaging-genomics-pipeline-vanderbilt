import pandas as pd 
import numpy as np 
import sciluigi as sl

from src.utils.filesystem import create_path_if_not_exists
from src.config.Config import Config

class FormatPhensAndCovsTask(sl.Task):
	"""
	Format phenotypes to adhere to the BGENIE style. 

	source: https://jmarchini.org/bgenie/

	- Nhung, April 2023 (updated Feb 2024)
	"""
	group = sl.Parameter()
	basepath = sl.Parameter()
	done = False


	def out_format_phens_and_covs(self):
		# Output target for formatted phenotypes and covariates	
		return sl.TargetInfo(self, f'{self.basepath}/{Config.GWAS_FORMAT_OUT_PATH.replace("GROUP_NAME", self.group)}')

	def requires(self):
		pass


	def run(self):
		# TODO - NEED TO ADD logic to handle the following case
		## NOTE: Specifically for the random data I've shared with Metacell, I manually 
		## updated the output phenotype and covariate files such that the FID and IID of 
		## the first subject is now 1000 instead of 0. This is because plink2 (required 
		## for other steps) doesn't allow FID/IID to be 0. 

		group = self.group

		coho_path = Config.COHORT_PATH.replace('GROUP_NAME', group)
		phen_path = Config.PHEN_PATH.replace('GROUP_NAME', group)
		covs_path = Config.COVS_PATH.replace('GROUP_NAME', group)

		out_path = str(self.out_format_phens_and_covs().path)
		phen_out_path = f'{out_path}/{Config.PHEN_OUT_PATH}'
		covs_out_path = f'{out_path}/{Config.COVS_OUT_PATH}'

		create_path_if_not_exists(out_path)
		create_path_if_not_exists(f'{out_path}/phenotypes')  ## since phen_path is inside phenotypes folder

		coho = pd.read_csv(coho_path, sep='\t', header=None)[0].values

		phen_data = pd.read_csv(phen_path, sep='\t', index_col='eid')
		covs_data = pd.read_csv(covs_path, sep='\t', index_col='eid')

		assert(np.array_equal(coho, phen_data.index.values))
		assert(np.array_equal(coho, covs_data.index.values))

		phen_data.index.rename('FID', inplace=True)
		phen_data.insert(0, 'IID', coho)

		covs_data.index.rename('FID', inplace=True)
		covs_data.insert(0, 'IID', coho)

		phen_data.to_csv(phen_out_path, sep=' ')
		covs_data.to_csv(covs_out_path, sep=' ')

		self.done = True

	def complete(self):
		return self.done


if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()
		group = sl.Parameter()

		def workflow(self):
			format_phens_and_covs_task = self.new_task('format_phens_and_covs_task', FormatPhensAndCovsTask, group=self.group, basepath=self.basepath)
			return format_phens_and_covs_task
		
	sl.run_local(main_task_cls=Workflow)
