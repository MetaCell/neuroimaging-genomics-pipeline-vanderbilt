
import numpy as np
import pandas as pd
import h5py
import sys
import sciluigi as sl
from statsmodels.regression.linear_model import OLS as OLS
from statsmodels.tools.tools import add_constant
from statsmodels.stats.multitest import multipletests as sm
from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists
import os

class TwasStatsTask(sl.Task):
	"""
	Single-gene stats for polygenic comparison. 

	Run TWAS to get the r^2 values (p-value should 
	match the PrediXcan Association version). Per 
	regional phenotype, store matrix with dimensions 

	(genes, [r^2, pval, FDR threshold, Bonferroni threshold])

	The thresholds should be the same across genes of a 
	given regional phenotype. 
	"""

	group = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_twas_stats(self):
		# Output target for TWAS stats
		return sl.TargetInfo(self, f'{self.basepath}')

	def requires(self):
		pass


	## func: fit and report single-gene regression 
	def regression(self, reg, phen, gidx, grex_all, phen_all, sin_data):

		## single-gene data 
		gg = grex_all[(reg,phen)][:,gidx] ## (subjs,)
		pp = phen_all[(reg,phen)] ## (subjs,)

		## for OLS: add intercept constant
		gg = add_constant(gg)

		## fit regression model
		model = OLS(pp, gg).fit()
		r2 = model.rsquared
		pv = model.pvalues[1]

		#print('tw: {}\nnh: {}\n'.format(,pv))
		n = sin_data[(reg,phen)][1]['unc'][gidx]
		h = pv 
		# print(n.round(6), h.round(6))
		# assert(n.round(6) == h.round(6))

		return r2, pv



	def run(self):
		group = self.group

		regions = Config.REG_NAMES
		phens = Config.COMMON_PHENS
		reg_phens = [(r,p) for r in regions for p in phens]


		out_twas_stats = str(self.out_twas_stats().path)

		## paths
		twas_path = f'{out_twas_stats}/{Config.POLY_TWAS_PATH}'.replace('GROUP_NAME', self.group)  ## will need to replace REGION_NAME below 
		grex_path = f'{out_twas_stats}/{Config.POLY_GREX_PATH}'.replace('GROUP_NAME', self.group)  ## will need to replace REGION_NAME below
		phen_path = f'{out_twas_stats}/{Config.POLY_PHEN_PATH}'.replace('GROUP_NAME', self.group) 
		out_path = f'{out_twas_stats}/{Config.POLY_STATS_OUTPUT_PATH}'.replace('GROUP_NAME', self.group)

		twas_stat_outs_path = f'{out_twas_stats}/{Config.TWAS_STATS_OUTPUT_PATH}'.replace('GROUP_NAME', self.group)
		create_path_if_not_exists(out_path)


		## load grex and phen data
		grex_all = {} ## k: (reg, phen), v: (subj * gene)
		phen_all = {} ## k: (reg, phen), v: (subj,)

		## init outputs
		sin_data = {} ## k: (reg, phen), v: ([gene], [twas pval])
		sin_sigs = {} ## k: (reg, phen), v: {ben, bon}

		for (reg, phen) in reg_phens: 
			# ADDED - @d-gopalkrishna - so if phens do not exist - we continue with the ones that exist without error
			if not os.path.exists(phen):
				continue

			## get significant TWAS genes 
			tfile = twas_path.replace('REGION_NAME', reg).replace('PHEN_TYPE', phen)
			df = pd.read_table(tfile, sep='\t', usecols=['gene', 'pvalue'])

			abar = 0.1 ## default should be 0.05, but can be specified by user
			bon_keep, bons, _, bon_line = sm(df['pvalue'], method='bonferroni', alpha=abar)
			ben_keep, bens, _, _ = sm(df['pvalue'], method='fdr_bh', alpha=abar)

			sin_sigs[(reg,phen)] = {'bon_line': bon_line, 'ben_line': df['pvalue'][ben_keep].max()}

			df['bon'] = bons
			df['ben'] = bens

			pbar = 0.05

			keep = (df['pvalue'] < pbar)
			df_keep = df.loc[keep]
			twas_genes = df_keep['gene'].values
			twas_pvals = df_keep['pvalue'].values

			twas_bons = df_keep['bon'].values
			twas_bens = df_keep['ben'].values

			## get grex matrices and slice 
			gpath = grex_path.replace('REGION_NAME', reg)
			with h5py.File(gpath, 'r') as f:
				reg_gene = f['genes'][()].astype(str)
				grex_mat = f['pred_expr'][()]

			gset, idx1, idx2 = np.intersect1d(reg_gene, twas_genes, return_indices=True)
			grex_all[(reg, phen)] = grex_mat[idx1].T
			sin_data[(reg, phen)] = (gset, {'unc': twas_pvals[idx2], \
											'bon': twas_bons[idx2], \
											'ben': twas_bens[idx2]}) 

			## get phenotype arrays 
			ppath = phen_path.replace('PHEN_TYPE', phen)
			df = pd.read_table(ppath, sep='\t', usecols=[reg])
			phen_all[(reg,phen)] = df[reg].values



		# ----------
		## main loop 
		sin_stats = {} ## k: (reg,phen), v: genes * [r2, pv, ben, bon]
		for (reg, phen) in reg_phens: 
			# ADDED - @d-gopalkrishna - so if phens do not exist - we continue with the ones that exist without error
			if not os.path.exists(phen):
				continue

			nsig = sin_data[(reg,phen)][0].size
			r2s = np.zeros((nsig,1))
			pvs = np.zeros((nsig,1))
			bhs = np.zeros((nsig,1))
			bfs = np.zeros((nsig,1))

			for i in range(nsig): 
				r2, pv = self.regression(reg, phen, i, grex_all, phen_all, sin_data)
				r2s[i][0] = r2
				pvs[i][0] = pv
				bhs[i][0] = sin_data[(reg,phen)][1]['ben'][i]
				bfs[i][0] = sin_data[(reg,phen)][1]['bon'][i]

			results = np.concatenate([r2s, pvs, bhs, bfs], axis=1)
			sin_stats[(reg,phen)] = results 

		with h5py.File(twas_stat_outs_path, 'w') as f: 
			for (reg, phen), stats in sin_stats.items(): 
				key = '{}X{}'.format(reg,phen)
				f[key] = stats

		self.done = True

	def complete(self):
		return self.done 


if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			run_twas_stats = self.new_task('run_twas_stats', TwasStatsTask, group=self.group, basepath=self.basepath)
			return run_twas_stats

		
	sl.run_local(main_task_cls=Workflow)
