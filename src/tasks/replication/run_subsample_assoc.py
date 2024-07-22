import sciluigi as sl
import os
import subprocess
from multiprocessing import Pool

from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists

class RunSubSamplesAssocTask(sl.Task):
	"""
	Script for running PrediXcan Association
	on a random subsample of UKB to match  
	the sample size of HCP data.
	"""

	basepath = sl.Parameter()
	done = 	False

	def out_subsamples_assoc(self):
		# Output target for subsamples path
		return sl.TargetInfo(self, f'{self.basepath}/{Config.REPLICATION_OUTPATH}/')

	def requires(self):
		# return SaveSubsamplesTask()
		pass

	def run(self):
		twas_script = f'{Config.METAXCAN_PATH}/software/nh_PrediXcanAssociation.py'
		grex_path = f'{Config.POLY_GREX_PATH}'.replace('GROUP_NAME', 'UKB')
		phen_file = f'{Config.POLY_PHEN_PATH}'.replace('GROUP_NAME', 'UKB') \
			.replace('PHEN_TYPE', 'vol_mean')
		covs_file = f'{Config.COVS_FILE}'.replace('GROUP_NAME', 'UKB')

		out_dir = str(self.out_subsamples_assoc().path)
		create_path_if_not_exists(out_dir)

		brain_names = Config.REG_NAMES
		covs = ['age', 'isMale']

		for i in range(1, 41):
			covs.append(f'PC{i}')

		# dsizes = [772, 2000, 5000, 15000]    # -> why is both used. the one after replaces it
		dsizes = [5000]

		for itr in range(100):
			for dsize in dsizes:
				for idx in range(len(brain_names)):
					print(f'[{itr}] {brain_names[idx]}')

					if itr % 3 == 0 and brain_names[idx] == 'dlpfc':
						subprocess.run([
							'nice', '-n', '18'
							'python', '-u', twas_script,
							'--input_phenos_file', phen_file,
							'--input_phenos_column', brain_names[idx],
							'--covariates_file', covs_file,
							'--covariates', ' '.join(covs),
							'--sample_iter', f'{dsize}_{itr}',
							'--output', f'{out_dir}/{dsize}c_{itr}_{brain_names[idx]}.txt'
						])
					else:
						subprocess.run([
							'nice', '-n', '18',
							'python', '-u', twas_script,
							'--hdf5_expression_file', f'{grex_path}/{brain_names[idx]}.hdf5',
							'--input_phenos_file', phen_file,
							'--input_phenos_column', brain_names[idx],
							'--covariates_file', covs_file,
							'--covariates', ' '.join(covs),
							'--sample_iter', f'{dsize}_{itr}',
							'--verbosity', '100',
							'--output', f'{out_dir}/{dsize}c_{itr}_{brain_names[idx]}.txt'
						])
		self.done = True

	def complete(self):
		return self.done
	

if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()

		def workflow(self):
			run_save_subsample_assoc = self.new_task('run_save_subsample_assoc', RunSubSamplesAssocTask, basepath=self.basepath)
			return run_save_subsample_assoc

		
	sl.run_local(main_task_cls=Workflow)
