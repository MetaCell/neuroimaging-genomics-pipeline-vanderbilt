
import pandas as pd  
import sciluigi as sl

import numpy as np
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests as sm

import sys 
import os

from time import time 
from multiprocessing import Pool

from src.config.Config import Config

class CompareGwasTwasTask(sl.Task):
	"""
	Concatentate the TWAS and GWAS results into one big table. 
	"""
	
	group = sl.Parameter()
	phens = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_compare_gwas_twas(self):
		return sl.TargetInfo(self, f'{self.basepath}')


	def requires(self):
		# TODO: add the previous sub steps here
		pass

		

	## get TWAS and GWAS data
	def get_data(self, reg, twas_path, gwas_path):
		
		print(f'starting on {reg}...')

		## phen, GWAS_FDR, GWAS_BON, TWAS_FDR, GWAS_BON
		sig_data = {'phenotype': [reg]}

		## read GWAS
		gwas_file = f'{gwas_path}_{reg}.regenie'
		gwas_data = pd.read_table(gwas_file, usecols=['ID', 'BETA', 'LOG10P'], sep=' ')
		gwas_data = gwas_data.rename(columns={'ID': 'rsid', 'BETA': 'beta', 'LOG10P': '-log10p'})

		pvals = gwas_data['-log10p']
		gwas_data['pval'] = np.power(10, -pvals)

		fkeep, fvals, _, _ = sm(gwas_data['pval'], method='fdr_bh', alpha=0.05)
		bkeep, bvals, _, alpha = sm(gwas_data['pval'], method='bonferroni', alpha=0.05)
		
		gwas_data['FDR'] = fvals
		gwas_data['BON'] = bvals  

		sig_data['GWAS_FDR'] = [gwas_data['pval'][fkeep].max()]
		sig_data['GWAS_BON'] = [alpha]

		## read TWAS
		twas_file = f'{twas_path}/{reg}.txt'
		twas_data = pd.read_table(twas_file, usecols=['gene', 'pvalue', 'effect'])
		twas_data = twas_data.rename(columns={'pvalue': 'pval', 'effect': 'beta'})

		fkeep, fvals, _, _ = sm(twas_data['pval'], method='fdr_bh', alpha=0.05)
		bkeep, bvals, _, alpha = sm(twas_data['pval'], method='bonferroni', alpha=0.05)
		
		twas_data['FDR'] = fvals
		twas_data['BON'] = bvals  

		sig_data['TWAS_FDR'] = [twas_data['pval'][fkeep].max()]
		sig_data['TWAS_BON'] = [alpha]

		gwas_data = gwas_data[['rsid', 'beta', 'pval', 'FDR', 'BON']]
		twas_data = twas_data[['gene', 'beta', 'pval', 'FDR', 'BON']]
		return gwas_data, twas_data, sig_data 

	## set region-specific tables 
	def set_tables(self, reg):
		wjti_path = f'{Config.WJTI_PATH}'
		out_compare_path = f'{self.out_compare_gwas_twas().path}'
		twas_path = f'{out_compare_path}/{Config.COMPARE_TWAS_PATH}'.replace('GROUP_NAME', self.group).replace('PHENS', self.phens)
		gwas_path = f'{out_compare_path}/{Config.COMPARE_GWAS_PATH}'.replace('GROUP_NAME', self.group).replace('PHENS', self.phens)

		summ_rtmp = f'{out_compare_path}/{Config.SUMM_RTMP}'.replace('GROUP_NAME', self.group)
		sigs_rtmp = f'{out_compare_path}/{Config.SIGS_RTMP}'.replace('GROUP_NAME', self.group)

		rstart = time()

		## get table of gene-snp pairings 
		mapp = pd.read_csv(f'{wjti_path}/{reg}.csv', usecols=['rsid', 'gene'])

		## get TWAS/GWAS data 
		gwas, twas, stable = self.get_data(reg, twas_path=twas_path, gwas_path=gwas_path)

		## set sig table
		stable = pd.DataFrame(stable)

		rtime = time() - rstart
		(hr, mn, sc) = (rtime//3600, (rtime%3600)//60, (rtime%3600)%60)
		print('{:d} hr {:d} mn {:d} sc to get data ({})'.format(int(hr), int(mn), int(sc), reg))

		## merge twas table with mapp (this should add rsids to the table) 
		rstart = time()
		mtable = twas.merge(mapp, on='gene', how='inner')

		## merge gwas table with the new table 
		rtable = mtable.merge(gwas, on='rsid', how='inner', suffixes=['_TWAS', '_GWAS'])

		## make sure we have all the TWAS genes 
		gene_left = np.setdiff1d(twas['gene'], rtable['gene'])
		twas_left = twas.loc[twas['gene'].isin(gene_left)]
		twas_left = twas_left.rename(columns={'beta': 'beta_TWAS', 'pval': 'pval_TWAS', \
											'FDR': 'FDR_TWAS', 'BON': 'BON_TWAS'})

		rtable = rtable.append(twas_left)
		rtable['phenotype'] = reg

		print(rtable.loc[rtable['FDR_TWAS'] <= 0.05]['gene'].drop_duplicates().shape, reg)

		## merge time
		rtime = time() - rstart
		(hr, mn, sc) = (rtime//3600, (rtime%3600)//60, (rtime%3600)%60)
		print('{:d} hr {:d} mn {:d} sc to merge ({})'.format(int(hr), int(mn), int(sc), reg))

		## save tables
		rstart = time()

		stable.to_csv(f'{sigs_rtmp}_{reg}.csv', index=False)
		rtable.to_csv(f'{summ_rtmp}_{reg}.csv', index=False)

		rtime = time() - rstart
		(hr, mn, sc) = (rtime//3600, (rtime%3600)//60, (rtime%3600)%60)
		print('{:d} hr {:d} mn {:d} sc to write table ({})'.format(int(hr), int(mn), int(sc), reg))

	def run(self):	
		out_compare_path = f'{self.out_compare_gwas_twas().path}'
		summ_path = f'{out_compare_path}/{Config.SUMM_PATH}'.replace('GROUP_NAME', self.group)
		sig_path = f'{out_compare_path}/{Config.SIG_PATH}'.replace('GROUP_NAME', self.group)

		summ_rtmp = f'{out_compare_path}/{Config.SUMM_RTMP}'.replace('GROUP_NAME', self.group)
		sigs_rtmp = f'{out_compare_path}/{Config.SIGS_RTMP}'.replace('GROUP_NAME', self.group)


		regs = Config.GWAS_REGS
		
		pool = Pool(processes=len(regs))
		pool.map(self.set_tables, regs)

		## concat regional TWAS/GWAS summaries
		r0 = regs[0]
		cmd = f'cp {summ_rtmp}_{r0}.csv {summ_path}'	
		os.system(cmd)
		for reg in regs[1:]: 
			cmd = f'tail -n +2 {summ_rtmp}_{reg}.csv >> {summ_path}'
			os.system(cmd)

		## concat regional sigs summaries
		cmd = f'cp {sigs_rtmp}_{r0}.csv {sig_path}'
		os.system(cmd)
		for reg in regs[1:]: 
			cmd = f'tail -n +2 {sigs_rtmp}_{reg}.csv >> {sig_path}'
			os.system(cmd)

		self.done = True

	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		phens = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			compare_gwas_twas_task = self.new_task('compare_gwas_twas_task', CompareGwasTwasTask, group=self.group, basepath=self.basepath, phens=self.phens)
			return compare_gwas_twas_task
	
	sl.run_local(main_task_cls=Workflow)

