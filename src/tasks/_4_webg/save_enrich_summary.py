import sciluigi as sl
import logging
import os
from multiprocessing import Pool
import numpy as np
import pandas as pd 
import sys 
from src.utils.filesystem import create_path_if_not_exists

from src.config.Config import Config

# Init logging
log = logging.getLogger('sciluigi-interface')


class SaveEnrichSummaryTask(sl.Task):
	"""
	Save the summary of the enrichment results.
	"""

	enrich = sl.Parameter()
	group = sl.Parameter()
	phens = sl.Parameter()
	ptype = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_save_enrich_summary(self):
		# Output target for enrichment summary
		return sl.TargetInfo(self, f'{self.basepath}')


	def requires(self):
		pass

	def run(self):
		enrich = self.enrich
		phens = self.phens
		out_path_enr_sum = str(self.out_save_enrich_summary().path)


		enr_path = f'{out_path_enr_sum}/{Config.ENR_PATH}'.replace('GROUP_NAME', self.group).replace('ENRICH_NAME', self.enrich) \
			.replace('PTYPE', self.ptype).replace('PHENS', self.phens)    ## _{reg}.txt 
		out_path = f'{out_path_enr_sum}/{Config.ENR_OUT_PATH}'.replace('GROUP_NAME', self.group).replace('ENRICH_NAME', self.enrich) \
			.replace('PTYPE', self.ptype).replace('PHENS', self.phens)


		create_path_if_not_exists(out_path_enr_sum)

		cols = ['geneSet', 'description', 'size', 'overlap', 'enrichmentRatio', 'pValue', 'FDR']
		name = ['annotation', 'description', 'num annot genes', \
				'pheno-annot overlap', 'enrichment ratio', 'pvalue', 'FDR']
		cdict = {c: n for c, n in zip(cols, name)}

		regs = Config.ENRICH_SUMMARY_REGS

		summ = None
		for reg in regs:
			df = pd.read_table(f'{enr_path}_{reg}.txt', usecols=cols).rename(columns=cdict)

			## temp bandaid
			if enrich == 'gwas_catalog': 
				df['annotation'] = df['annotation'].apply(lambda x: x.split(' | ')[0])
				df['description'] = df['description'].apply(lambda x: x.split(' | ')[1])
			##

			df.insert(3, 'twas phenotype', reg)

			if summ is None: summ = df
			else: summ = pd.concat([summ, df])

		summ.to_csv(out_path, index=False)

		self.done = True

	
	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		enrich = sl.Parameter()
		phens = sl.Parameter()
		ptype = sl.Parameter()
		basepath = sl.Parameter()
		group = sl.Parameter()

		def workflow(self):
			run_enrichment_summary = self.new_task('run_enrichment_summary', SaveEnrichSummaryTask, group=self.group, enrich=self.enrich, phens=self.phens, ptype=self.ptype, basepath=self.basepath)
			return run_enrichment_summary
		
	# Run the workflow
	sl.run_local(main_task_cls=Workflow)
		
