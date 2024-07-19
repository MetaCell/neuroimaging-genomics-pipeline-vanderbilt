import sciluigi as sl
from src.config.Config import Config
import subprocess
from src.utils.filesystem import create_path_if_not_exists


class GetQCStatsTask(sl.Task):

	basepath = sl.Parameter()
	group = sl.Parameter()
	done = False

	def out_get_qc_stats(self):
		# Output target for QC stats
		return sl.TargetInfo(self, f'{self.basepath}/{Config.GWAS_QC_OUT_PATH}'.replace('GROUP_NAME', self.group))

	def requires(self):
		pass

	def save_new_chr_files(self, chr_num, qc_outs_path):
		bgen_raw = f'{Config.BGEN_RAW_PATH}/c{chr_num}.bgen'.replace('GROUP_NAME', self.group)
		sample_path = f'{Config.BGEN_RAW_PATH}/c{chr_num}.sample'.replace('GROUP_NAME', self.group)

		hard_call_threshold = '0.1'
		qc_out_path = f'{self.out_get_qc_stats().path}'
		out_path = f'{qc_out_path}/c{chr_num}'
		cmd = [
			Config.PLINK_PATH, '--bgen', bgen_raw, 'ref-first', '--sample', sample_path,
			'--snps-only', '--hard-call-threshold', hard_call_threshold, 
			'--make-pgen', '--out', out_path
		]

		result = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			check=False
		)
		print(result.stdout)
		print(result.stderr)

	def apply_filters_for_missingness(self, chr_num, qc_out_path):
		qc_out_path = f'{self.out_get_qc_stats().path}'
		pfile_path = f'{qc_out_path}/c{chr_num}'
		geno = str(0.05)
		maf = str(0.01)
		out_path = f'{qc_out_path}/c{chr_num}'

		cmd = [
			Config.PLINK_PATH, '--pfile', pfile_path, '--geno', geno,
			'--maf', maf, '--make-pgen', '--out', out_path
		]

		result = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			check=True
		)
		print(result.stdout)
		print(result.stderr)


	def remove_duplicate_snps(self, chr_num, qc_outs_path):
		qc_out_path = f'{self.out_get_qc_stats().path}'
		pfile_path = f'{qc_out_path}/c{chr_num}'
		hwe = str(0.00001)
		qc_out_path = f'{self.out_get_qc_stats().path}'
		out_path = f'{qc_out_path}/c{chr_num}'

		cmd = [
			Config.PLINK_PATH, '--pfile', pfile_path, '--rm-dup', 'exclude-mismatch',
			'--hwe', hwe, '--export', 'bgen-1.2', 'bits=8', '--out', out_path
		]

		result = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			check=True
		)
		print(result.stdout)
		print(result.stderr)


	def index_bgen_files(self, chr_num, qc_outs_path):
		bgen_file_path = f'{Config.BGEN_RAW_PATH}/c{chr_num}.bgen'.replace('GROUP_NAME', self.group)

		cmd = [
			Config.BGENIX_PATH, '-g', bgen_file_path, '-index',
			'-clobber'
		]

		result = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			check=True
		)
		print(result.stdout)
		print(result.stderr)

		# # once indexed copy and paste to the output directory
		# cmd = [
		# 	'cp', f'{bgen_file_path}.bgi', f'{self.out_get_qc_stats().path}/c{chr_num}.bgen.bgi'
		# ]

	def run(self):
		qc_outs_path = f'{self.out_get_qc_stats().path}'
		create_path_if_not_exists(qc_outs_path)

		for chr in range(1, 23):
			self.save_new_chr_files(chr, qc_outs_path)
			self.apply_filters_for_missingness(chr, qc_outs_path)
			self.remove_duplicate_snps(chr, qc_outs_path)
			self.index_bgen_files(chr, qc_outs_path)

		self.done = True

	def complete(self):
		return self.done


if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()
		group = sl.Parameter()

		def workflow(self):
			get_qc_stats_task = self.new_task('get_qc_stats_task', GetQCStatsTask, basepath=self.basepath, group=self.group)
			return get_qc_stats_task
		
	sl.run_local(main_task_cls=Workflow)
