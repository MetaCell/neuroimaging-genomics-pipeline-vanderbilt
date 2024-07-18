import sciluigi as sl
import logging
import os
from multiprocessing import Pool
import numpy as np
import pandas as pd 
import sys

from statsmodels.stats.multitest import multipletests as sm
from src.utils.filesystem import create_path_if_not_exists
from src.config.Config import Config
from src.tasks._2_twas.clean_twas import CleanTwasTask

# Init logging
log = logging.getLogger('sciluigi-interface')

class ConcatTwasTask(sl.Task):
	"""
	Concatenate TWAS output files.
	"""

	group = sl.Parameter()
	phens = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_concat(self):
		# Output target for concatenated twas path
		return sl.TargetInfo(self, f'{self.basepath}/{Config.CONCAT_TWAS_OUTPUT_PATH}' \
					   .replace('GROUP_NAME', self.group))

	def requires(self):
		return CleanTwasTask(cohort=self.group, basepath=self.basepath, workflow_task=self.workflow_task, instance_name='CleanTwasTask')

	def run(self):
		group = self.group
		phens = self.phens

		regs = Config.TWAS_REGS
		twas_path =Config.TWAS_PATH.replace('GROUP_NAME', group).replace('PHENS', phens)
		itwa_path =Config.ITWA_PATH.replace('GROUP_NAME', group).replace('PHENS', phens)
		gene_path =Config.GENE_PATH
		# outs_path =Config.OUTS_PATH.replace('GROUP_NAME', group)
		outs_path = str(self.out_concat().path)
		outs_csv_file = f'{outs_path}/summary.csv'

		# read ens-to-sym map
		ens2sym = pd.read_csv(gene_path, index_col='ens').to_dict()['sym']

		# reg loop
		rlist = [(gr, pr) for gr in regs for pr in regs]
		tcols = {'gene': 'ens', 'pvalue': 'pval', 'effect': 'beta'}

		dfs = []

		create_path_if_not_exists(outs_path)
		for (gr, pr) in rlist:

			if gr == pr: tfile = f'{twas_path}/{gr}.txt'
			else: tfile = f'{itwa_path}/grex_{gr}_phen_{pr}.txt'

			# gene names
			df = pd.read_table(tfile, usecols=tcols.keys())
			df = df.rename(columns=tcols)
			df['sym'] = df['ens'].map(ens2sym)

			# pvalues
			df['FDR'] = sm(df['pval'], method='fdr_bh', alpha=0.05)[1]
			df['BON'] = sm(df['pval'], method='bonferroni', alpha=0.05)[1]

			# grex and phen
			df['grex'] = gr
			df['phen'] = pr

			dfs.append(df)

		# save
		df = pd.concat(dfs)
		cols = Config.TWAS_COLUMN_NAMES
		df = df[cols]
		df.to_csv(outs_csv_file, index=False)

		self.done = True

	def complete(self):
		return self.done


if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		phens = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			conc_twas_task = self.new_task('conc_twas', ConcatTwasTask, group=self.group, phens=self.phens, basepath=self.basepath)
			return conc_twas_task
		
	sl.run_local(main_task_cls=Workflow)
