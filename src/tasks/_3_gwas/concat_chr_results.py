import sciluigi as sl
from src.config.Config import Config
import subprocess
from src.utils.filesystem import create_path_if_not_exists
import os


class ConcatChrResults(sl.Task):
	"""
	Concat regenie chr results into one file. 
	"""
	group = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_concat_chr_results(self):
		# Output target 
		return sl.TargetInfo(self, f'{self.basepath}/{Config.GWAS_RUN_REGENIE_OUTPUT_PATH}'.replace('GROUP_NAME', self.group))

	def requires(self):
		pass

	def run(self):
		regs = Config.GWAS_REGS
		gwas_ipath =  f'{self.out_concat_chr_results().path}'
		create_path_if_not_exists(gwas_ipath)

		for reg in regs:
			source_file = f'{gwas_ipath}/s2_c1_{reg}.regenie'
			dest_file = f'{gwas_ipath}/vol_mean_{reg}.regenie'
			subprocess.run(
				[
					'cp', 
					source_file,
					dest_file
				],
				capture_output=True,
				text=True,
				check=True
			)
			print(reg)

			for chr in range(2, 23):
				source_file = f'{gwas_ipath}/s2_c{chr}_{reg}.regenie'
				dest_file = f'{gwas_ipath}/vol_mean_{reg}.regenie'

				cmd = [
					'tail', '-n', '+2', 
					source_file,
					'>>',
					dest_file
				]
				os.system(' '.join(cmd))
				print(chr)

		self.done = True

	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		basepath = sl.Parameter()


		def workflow(self):
			run_concat_chr = self.new_task('run_concat_chr', ConcatChrResults, group=self.group, basepath=self.basepath)
			return run_concat_chr
		
	sl.run_local(main_task_cls=Workflow)
