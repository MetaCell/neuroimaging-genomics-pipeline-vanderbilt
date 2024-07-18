import sciluigi as sl
import logging
import os
from multiprocessing import Pool
import numpy as np
import pandas as pd

from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists


# Init logging
log = logging.getLogger('sciluigi-interface')


class SavePredixvuGMTTask(sl.Task):
	"""
	Save PrediXVU ontology based on 
	nominal p < 0.001 for WebGestalt. 
	"""
	basepath = sl.Parameter()
	done = False

	def out_save_predixvu_gmt(self):
		# Output target for PrediXVU GMT file
		return sl.TargetInfo(self, f'{self.basepath}/{Config.WEBG_PREDIXVU_OUTPUT_PATH}')


	def requires(self):
		pass

	def run(self):
		## phecodes to remove (non-specific) 
		phe_rm = Config.PHE_RM
		brn_rm = Config.BRN_RM
		brn_rm = [f'Brain_{b}_combo' for b in brn_rm] 

		## paths 
		pdx_path = f'{Config.WEBG_PDX_PATH}'
		phe_path = f'{Config.WEBG_PHE_PATH}'

		## out paths 
		predixvu_out_path = str(self.out_save_predixvu_gmt().path)
		create_path_if_not_exists(predixvu_out_path)
		des_path = f'{predixvu_out_path}/pdx_nom0.001.des'
		gmt_path = f'{predixvu_out_path}/pdx_nom0.001.gmt' 


		## read table and filter 
		cols = ['ensembl', 'phecode', 'p-value', 'tissue']
		df = pd.read_csv(pdx_path, usecols=cols)

		df = df.loc[df['p-value'] < 0.001] 
		df = df.loc[df['tissue'].str.contains('Brain')]
		df = df.loc[~df['tissue'].isin(brn_rm)]

		df = df[['ensembl', 'phecode']].drop_duplicates()
		df = df.loc[~df['phecode'].isin(phe_rm)]

		## get phecode gene lists and save .gmt  
		glists = df.groupby('phecode')['ensembl'].apply(list)

		lines = [] 
		for phecode, glist in glists.items(): 
			genes = '\t'.join(glist)
			line = f'{phecode}\tNA\t{genes}\n'
			lines.append(line)

		with open(gmt_path, 'w') as f: 
			f.writelines(lines)

		## save .des 
		df = pd.read_csv(phe_path, usecols=['phecode', 'phenotype'])    
		df = df.loc[df['phecode'].isin(glists.index.values)]

		df.to_csv(des_path, sep='\t', index=False, header=False)

		self.done = True

	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()
		
		def workflow(self):
			save_predixvu_gmt = self.new_task('save_predixvu_gmt', SavePredixvuGMTTask, basepath=self.basepath)
			return save_predixvu_gmt
		
	sl.run_local(main_task_cls=Workflow)