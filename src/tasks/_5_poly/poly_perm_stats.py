import numpy as np
import pandas as pd
import h5py
import sys
import sciluigi as sl
from scipy.stats import pearsonr
from src.config.Config import Config
import os
from src.utils.filesystem import create_path_if_not_exists

from statsmodels.regression.linear_model import OLS as OLS
from statsmodels.tools.tools import add_constant

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from multiprocessing import Pool 
import logging

# Init logging
log = logging.getLogger('sciluigi-interface')


class PolyPermStatsTask(sl.Task):
	"""
	Permutation version of polygenic analysis. 

	Per regional phenotype, a permutation is regression 
	fit to a random set of genes (size equal to 
	TWAS p < 0.001 genes). 

	Run N permutations per regional phenotype. 

	Save matrix of test r2s with shape (num_nulls, num_splits).
	"""
	
	group = sl.Parameter()
	basepath = sl.Parameter()
	done = False

	def out_poly_perm_stats(self):
		# Output target for permuted stats
		return sl.TargetInfo(self, f'{self.basepath}')


	def requires(self):
		pass

	## func: fit regression model on training cohort
	##       and evaluate on test cohort
	def regression(self, itr, grex_mat, phen_arr, train_masks):

		## get train/test split 
		train_mask = train_masks[itr]
		testt_mask = ~train_mask

		## get phen data
		ytrain = phen_arr[train_mask]
		ytestt = phen_arr[testt_mask]

		## get grex data
		xtrain = grex_mat[train_mask]
		xtestt = grex_mat[testt_mask]

		## for OLS: add intercept constant
		xtrain = add_constant(xtrain)
		xtestt = add_constant(xtestt)

		## fit multi-variate regression to
		## training data then get test data outputs
		model = OLS(ytrain, xtrain).fit()
		ptestt = model.predict(xtestt)

		## fit regression to test data output
		ptestt = add_constant(ptestt)
		model2 = OLS(ytestt, ptestt).fit()
		r2 = model2.rsquared

		return r2

	## func: permutation pool 
	def pool_run(self, reg_phen_null_xtimes): 
		print("pooling", reg_phen_null_xtimes)
		## pool params 
		(reg, phen, null, xtimes, num_split, grex_all, gene_num, phen_all, ntmp_path, train_masks) = reg_phen_null_xtimes 
		
		perm_rs = np.zeros((xtimes, num_split))
		
		for pidx in range(xtimes): 
			
			## get a rand list of genes
			rng = np.random.RandomState()
			grex = grex_all[reg]
			idxs = np.arange(grex.shape[1])
			gidx = rng.choice(idxs, gene_num[(reg,phen)], replace=False)

			## get grex and phen
			grex_mat = grex[:, gidx]
			phen_arr = phen_all[(reg,phen)]

			## get pearsons based on splits
			perm_rs[pidx] = [self.regression(i, grex_mat, phen_arr, train_masks) for i in range(num_split)]

		## tmp save 
		tfile = f'{ntmp_path}/{phen}_{reg}_{null}.hdf5'
		with h5py.File(tfile, 'w') as f: 
			f['split_r2s'] = perm_rs 
		print(phen, reg, null, '\n')


	def run(self):
		group = self.group
		num_split = None ## num of unique HCP fams
		regs = Config.REG_NAMES
		phens = Config.COMMON_PHENS
		reg_phens = [(r,p) for r in regs for p in phens]

		out_poly_perm_stats = str(self.out_poly_perm_stats().path)

		## paths
		subj_path = f'{Config.POLYPERM_SUBJ_PATH}'.replace('GROUP_NAME', self.group)
		fams_path = f'{Config.POLYPERM_FAMS_PATH}'.replace('GROUP_NAME', self.group)

		twas_path = f'{out_poly_perm_stats}/{Config.POLYPERM_TWAS_PATH}'.replace('GROUP_NAME', self.group)  ## will need to replace REGION_NAME below 
		grex_path = f'{out_poly_perm_stats}/{Config.POLYPERM_GREX_PATH}'.replace('GROUP_NAME', self.group)  ## will need to replace REGION_NAME below
		phen_path = f'{out_poly_perm_stats}/{Config.POLYPERM_PHEN_PATH}'.replace('GROUP_NAME', self.group) 

		## out paths
		out_path = f'{out_poly_perm_stats}/{Config.POLY_STATS_OUTPUT_PATH}'.replace('GROUP_NAME', self.group)

		ntmp_path = f'{out_poly_perm_stats}/{Config.POLYPERM_NTMP_PATH}'.replace('GROUP_NAME', self.group)
		null_path = f'{out_poly_perm_stats}/{Config.POLYPERM_NULL_PATH}'.replace('GROUP_NAME', self.group)

		create_path_if_not_exists(out_path)
		create_path_if_not_exists(ntmp_path)


		## load subject array
		subj_arr = pd.read_csv(subj_path, sep='\t', header=None)[0].values

		## load family IDs
		df = pd.read_csv(fams_path, usecols=['eid', 'family_id'], index_col='eid')
		df = df.reindex(subj_arr)
		subj_fids = df['family_id'].values
		uniq_fids = np.unique(subj_fids)

		num_split = uniq_fids.size * 2

		## split group into train and test sets
		train_masks = {} ## k: itr, v: mask
		for i in range(num_split):
			train_fids, _ = train_test_split(uniq_fids, \
							test_size=0.2, \
							random_state=i*150)
			train_masks[i] = np.isin(subj_fids, train_fids)

		## load grex and phen data
		grex_all = {} ## k: reg, v: (subj * gene)
		phen_all = {} ## k: (reg, phen), v: (subj,)
		gene_num = {} ## k: (reg, phen), v: num of sig genes 

		for phen in phens: 
			# ADDED - @d-gopalkrishna - so if phens do not exist - we continue with the ones that exist without error
			if not os.path.exists(phen):
				continue
			pfile = phen_path.replace('PHEN_TYPE', phen)
			pdf = pd.read_table(pfile, sep='\t')


			for reg in regs: 

				## store regional phen values 
				phen_all[(reg,phen)] = pdf[reg].values

				## store num of genes with TWAS p < 0.001
				tfile = twas_path.replace('REGION_NAME', reg).replace('PHEN_TYPE', phen)
				tdf = pd.read_table(tfile) 

				pbar = 0.05 ## should be a changable parameter
				num = np.sum(tdf['pvalue'] < pbar)

				gene_num[(reg,phen)] = num 
				print(f'{num} genes for {reg} {phen}')

				## store regional grex
				if phen != phens[0]: continue 
				gfile = grex_path.replace('REGION_NAME', reg)
				with h5py.File(gfile, 'r') as f:
					grex_mat = f['pred_expr'][()]
				grex_all[reg] = grex_mat.T



		# -----------
		## pool calls 
		xtimes = 5
		num_nulls = 10
		params = [(r,p,i,xtimes,num_split, grex_all, gene_num, phen_all, ntmp_path,train_masks) for r in regs for p in phens for i in range(num_nulls)]

		pool = Pool(processes=250)
		try:
			pool.map(self.pool_run, params)
		except:
			print("problemaa")
		finally:
			pool.close()
			pool.join()


		## concat results  
		stats = {} ## k: (regXphen), v: (nulls, splits)
		for (reg, phen) in reg_phens:
			# ADDED - @d-gopalkrishna - so if phens do not exist - we continue with the ones that exist without error
			if not os.path.exists(phen):
				continue

			rstats = np.zeros((num_nulls * xtimes, num_split))
			for n in range(num_nulls): 
				rfile = f'{ntmp_path}/{phen}_{reg}_{n}.hdf5'
				with h5py.File(rfile, 'r') as f: 
					s = n*xtimes; e = s+xtimes 
					rstats[s:e] = f['split_r2s'][()]

			stats[(reg,phen)] = rstats

		with h5py.File(null_path, 'w') as f:
			for (reg, phen), rstats in stats.items():
				f[f'{reg}X{phen}'] = rstats

		self.done = True

	
	def complete(self):
		return self.done



if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		group = sl.Parameter()
		basepath = sl.Parameter()

		def workflow(self):
			run_poly_perm_stats = self.new_task('run_poly_perm_stats', PolyPermStatsTask, group=self.group, basepath=self.basepath)
			return run_poly_perm_stats
		
	# Run the workflow
	sl.run_local(main_task_cls=Workflow)

