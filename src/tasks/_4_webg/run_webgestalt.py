
import logging
import os
import sciluigi as sl
import subprocess
from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists


# Init logging
log = logging.getLogger('sciluigi-interface')


class RunWebGestaltTask(sl.Task):
	"""
	This task runs the R script - run_webgestalt.R - to perform gene set enrichment analysis	
	"""

	group = sl.Parameter()   ## UKB
	ptype = sl.Parameter()   ## FDR
	phens = sl.Parameter()   ## vol_mean_interreg
	ontol = sl.Parameter()   ## pdx_nom0.001
	basepath = sl.Parameter()
	done = False

	def out_run_webgestalt(self):
		# Output target for WebGestalt results
		return sl.TargetInfo(self, f'{self.basepath}')
		

	def requires(self):
		pass

	def run(self):
		# install WebGestaltR using python subprocess
		# install_webgestalt_path = Config.INSTALL_WEBGESTALT_PATH
		# subprocess.call(
		# 	f"Rscript {install_webgestalt_path}",
		# )
		
		regs = Config.WEBG_REGS
		phens = self.phens
		out_path_webgestalt = str(self.out_run_webgestalt().path)
		create_path_if_not_exists(out_path_webgestalt)

		gmtPath = f'{out_path_webgestalt}/{Config.GMT_PATH}'.replace('ONTOL', self.ontol)
		desPath = f'{out_path_webgestalt}/{Config.DES_PATH}'.replace('ONTOL', self.ontol)
		jtiPath = f'{Config.WEBG_JTI_PATH}'
		innPath = f'{out_path_webgestalt}/{Config.WEBG_INN_PATH}'.replace('GROUP_NAME', self.group) \
			.replace('PTYPE', self.ptype).replace('PHENS', self.phens)
		
		outPath = f'{out_path_webgestalt}/{Config.WEBG_OUT_PATH}'.replace('GROUP_NAME', self.group) \
			.replace('PTYPE', self.ptype).replace('PHENS', self.phens).replace('ONTOL', self.ontol)
		
		run_webgestalt_path = Config.RUN_WEBGESTALT_PATH
		regs_parameter = ','.join(regs)
		result = subprocess.run([
			"Rscript", run_webgestalt_path, gmtPath, desPath, jtiPath, innPath, outPath, phens, regs_parameter
		],
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
		ptype = sl.Parameter()
		phens = sl.Parameter()
		ontol = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			run_webgestalt_task = self.new_task('run_webgestalt_task', RunWebGestaltTask, group=self.group, ptype=self.ptype, phens=self.phens, ontol=self.ontol, basepath=self.basepath)
			return run_webgestalt_task
		
	sl.run_local(main_task_cls=Workflow)