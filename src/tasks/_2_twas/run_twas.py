import sciluigi as sl
import os
import subprocess
from multiprocessing import Pool

from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists

class RunTwasTask(sl.Task):
	"""
	Script for running PrediXcan Association
	for regional or inter-regional associations. 
	"""
	basepath = sl.Parameter()
	group = sl.Parameter()
	model = sl.Parameter()
	which = sl.Parameter()   ## same or cross
	phens = sl.Parameter()
	done = False

	def out_twas(self):
		# Output target for twas path
		return sl.TargetInfo(self, f'{self.basepath}/{Config.TWAS_RUN_OUTPUT_PATH}' \
					   .replace('GROUP_NAME', self.group).replace('MODEL_NAME', self.model))

	def run(self):
		group = self.group
		model = self.model
		which = self.which
		phens = self.phens

		twas_script = Config.TWAS_SCRIPT

		grex_path=f'{self.basepath}/{Config.GREX_JTI_OUTPUT_PATH}'.replace('GROUP_NAME', group).replace('MODEL_NAME', model)
		phen_file=Config.PHEN_FILE.replace('GROUP_NAME', group).replace('TWAS_PHENS', phens)
		covs_file=Config.COVS_FILE.replace('GROUP_NAME', group)

		outs_dir=str(self.out_twas().path)
		
		
		brain_names = Config.BRAIN_NAMES
		covs = Config.COVS

		# Ensure output directory exists
		create_path_if_not_exists(outs_dir)

		log_dir = os.path.join(outs_dir, 'logs')
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)


		for i in range(1, 41):
			covs.append(f'PC{i}')

		if which == 'same':
			for idx in range(len(brain_names)):
				print(f"- {brain_names[idx]} -")
				hdf5_expression_file = f"{grex_path}/{brain_names[idx]}.hdf5"
				input_phenos_file = phen_file
				input_phenos_column = brain_names[idx]
				covariates_file = covs_file
				covariates = covs[idx]
				output = f"{outs_dir}/{phens}/{brain_names[idx]}.txt"
				
				cmd = [
					'python', '-u', twas_script,
					'--hdf5_expression_file', hdf5_expression_file,
					'--input_phenos_file', input_phenos_file,
					'--input_phenos_column', input_phenos_column,
					'--covariates_file', covariates_file,
					'--covariates', covariates,
					'--output', output
				]
				result = subprocess.run(
					cmd, capture_output=True,
					text=True,
					check=True
				)
				print(result.stdout)
				print(result.stderr)
		elif which == 'cross':
			for idx1 in range(len(brain_names)):
				for idx2 in range(len(brain_names)):
					if idx1 == idx2:
						continue

					b1 = brain_names[idx1]
					b2 = brain_names[idx2]

					print(f"- {b1} expr, {b2} phen -")
					hdf5_expression_file = f"{grex_path}/{b1}.hdf5"
					input_phenos_file = phen_file
					input_phenos_column = b2
					covariates_file = covs_file
					covariates = covs
					output = f"{outs_dir}/cross_regs/{phens}/grex_{b1}_phen_{b2}.txt"

					cmd = [
						'python', '-u', twas_script,
						'--hdf5_expression_file', hdf5_expression_file,
						'--input_phenos_file', input_phenos_file,
						'--input_phenos_column', input_phenos_column,
						'--covariates_file', covariates_file,
						'--covariates', covariates,
						'--output', output
					]
					result = subprocess.run(
						cmd, capture_output=True,
						text=True,
						check=True
					)
					print(result.stdout)
					print(result.stderr)
		else:
			# TODO: check if this is working
			return ValueError(f'Invalid value for which: {which}')

		self.done = True

	def complete(self):
		return self.done

if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()
		group = sl.Parameter()
		model = sl.Parameter()
		which = sl.Parameter()
		phens = sl.Parameter()

		def workflow(self):
			run_twas = self.new_task('run_twas', RunTwasTask, basepath=self.basepath, group=self.group, model=self.model, which=self.which, phens=self.phens)
			return run_twas
		
	sl.run_local(main_task_cls=Workflow)