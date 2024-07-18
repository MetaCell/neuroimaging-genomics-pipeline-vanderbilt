import sciluigi as sl
from src.config.Config import Config
import subprocess
from src.utils.filesystem import create_path_if_not_exists


class RunRegenieTask(sl.Task):
	"""
	Run regenie 
	"""
	group = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_run_regenie(self):
		# Output target for run regenie path
		return sl.TargetInfo(self, f'{self.basepath}/{Config.GWAS_RUN_REGENIE_OUTPUT_PATH}'.replace('GROUP_NAME', self.group))
		

	def requires(self):
		pass

	def run(self):
		regenie_path = f'{Config.REGENIE_PATH}'
		ipath = f'{self.basepath}/{Config.GWAS_IPATH_FROM_OUTPUT_PATH}'.replace('GROUP_NAME', self.group)
		cpath = f'{Config.GWAS_CPATH}'.replace('GROUP_NAME', self.group)
		ppath = f'{Config.GWAS_PPATH}'.replace('GROUP_NAME', self.group)

		opath =  f'{self.out_run_regenie().path}'
		create_path_if_not_exists(opath)


		for chr in range(22, 1, -1):
			cmd = [
				regenie_path,
				'--step', '1',
				'--bgen', f'{ipath}/c{chr}.bgen',
				'--covarFile', cpath,
				'--phenoFile', ppath,
				'--bsize', '1000',
				'--lowmem',
				'--lowmem-prefix', f'{opath}/mem_tmp_c{chr}',
				'--threads', '1',
				'--out', f'{opath}/c{chr}'
			]
			result = subprocess.run(
				cmd,
				capture_output=True,
				text=True,
				check=True
			)
			print(result.stdout)
			print(result.stderr)




		cmd = [
			regenie_path, '--step', '1', '--bgen', f'{ipath}/c1.bgen',
			'--covarFile', cpath, '--phenoFile', ppath, '--bsize', '1000',
			'--lowmem', '--lowmem-prefix', f'{opath}/mem_tmp_c1', '--threads', '1',
			'--out', f'{opath}/c1'
		]

		result = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			check=True
		)
		print(result.stdout)
		print(result.stderr)



		for chm in range(22, 0, -1):
			bgen_file_path = f'{ipath}/c{chm}.bgen'
			sample_file_path = f'{ipath}/c1.sample'
			pred_file_path = f'{opath}/c{chm}_pred.list'
			out_path = f'{opath}/s2_c{chm}'

			cmd = [
				regenie_path, '--step', '2', '--bgen', bgen_file_path,
				'--ref-first', '--sample', sample_file_path,
				'--covarFile', cpath, '--phenoFile', ppath,
				'--pred', pred_file_path, '--bsize', '1000',
				'--threads', '1', '--out', out_path
			]
			result = subprocess.run(
				cmd,
				capture_output=True,
				text=True,
				check=True
			)
			print(result.stdout)
			print(result.stderr)


		
		self.done = True

	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			run_regenie_task = self.new_task('run_regenie_task', RunRegenieTask, group=self.group, basepath=self.basepath)
			return run_regenie_task
		
	sl.run_local(main_task_cls=Workflow)
