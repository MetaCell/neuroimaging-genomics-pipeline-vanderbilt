import sciluigi as sl
import logging
import os
from multiprocessing import Pool
import numpy as np
from src.utils.filesystem import create_path_if_not_exists
from src.config.Config import Config
from src.tasks._2_twas.run_twas import RunTwasTask

# Init logging
log = logging.getLogger('sciluigi-interface')


class CleanTwasTask(sl.Task):
	"""
	Clean up TWAS output files.
	"""
	basepath = sl.Parameter()
	cohort = sl.Parameter()
	done = False

	def out_clean(self):
		# Not output for this step - this just cleans up the files
		pass

	def requires(self):
		# return RunTwasTask(cohort=self.cohort, basepath=self.basepath, workflow_task=self.workflow_task, instance_name='RunTwasTask')
		pass

	def run(self):
		cohort = self.cohort
		main_path = f'{Config.DATA_ROOT}/step_2/outputs'
		coho_path = f'{main_path}_{cohort}'

		tfiles = os.listdir(coho_path)
		# create_path_if_not_exists(str(self.out_clean().path))

		for t, tpath in enumerate(tfiles): 
			tfile = f'{coho_path}/{tpath}'

			# if file is a directory, skip
			if os.path.isdir(tfile): continue

			with open(tfile, 'r') as f: 
				lines = f.readlines()
				logging.info(f'Reading {tfile}, lines: {lines[1]}')

			if lines[1][0] != 'b': continue 

			new_lines = [lines[0]]
			for line in lines[1:]: 

				if '"' in line: 
					continue 

				if 'pheno' in line: 
					continue 

				if line[0] == 'b': 
					new_line = line.replace('b', '').replace("'", "")
					new_lines.append(new_line)

			# TODO: IF we go with the current style of how this works, it will replace the file with the new lines...
			# and old data will be lost. Should probably be appending to a new file.
			with open(tfile, 'w') as f: 
				logging.info(f'Writing to {tfile}')
				f.writelines(new_lines)

			if (t%100) == 0: 
				print('{} / {}'.format(t, len(tfiles)))

		self.done = True

	def complete(self):
		return self.done
		


if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		cohort = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			clean_twas_task = self.new_task('clean_twas', CleanTwasTask, cohort=self.cohort, basepath=self.basepath)
			return clean_twas_task
		
	sl.run_local(main_task_cls=Workflow)
