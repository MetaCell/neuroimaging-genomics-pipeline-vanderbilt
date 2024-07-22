import numpy as np 
import h5py  

from src.config.Config import Config

class SaveSubsamplesTask(sl.Task):
	"""
	Save random subsample indices for the UKB/HCP data. 
	"""

	def out_subsamples(self):
		# Output target for subsamples path
		pass

	def requires(self):
		pass
	
	def sample_UKB(self, main_path, n_shuffles=100):
		# TODO - move them to constants
		main_path = self.main_path
		UK_SAMPLES = 39565
		FULL_IDXS = np.arange(UK_SAMPLES).astype(int)
		opath = f'{main_path}_UKB/twas_repl_samples.hdf5'

		samp_idxs = {}
		disc_sizes = [772, 2000, 5000, 15000]

		# TODO: move to another method
		for dsc in disc_sizes:

			ds = UK_SAMPLES - dsc

			idxs = np.zeros((n_shuffles, ds), dtype=int)
			for i in range(n_shuffles):
				idx = np.random.choice(FULL_IDXS, ds, replace=False)
				idxs[i] = np.sort(idx)

			samp_idxs[dsc] = idxs
		
		# TODO: move to another method
		with h5py.File(opath, 'w') as f:
			for ds, idxs in samp_idxs.items():
				f[str(ds)] = idxs


	def sample_HCP(self, main_path, n_shuffles=100):
		ALL_EURO = 772
		NON_TWIN = 657
		
		opath = f'{main_path}_UKB/twas_repl_samples_HCPnonTwin.hdf5'
		

		FULL_IDXS = np.arange(39565).astype(int)
		SAMPLE_IDXS = np.zeros((n_shuffles, ALL_EURO), dtype=int)
		for i in range(n_shuffles):
			idx = np.random.choice(FULL_IDXS, ALL_EURO, replace=False)
			SAMPLE_IDXS[i] = np.sort(idx)

		with h5py.File(opath, 'w') as f:
			f['repl_idx'] = SAMPLE_IDXS


	def sample_UKB_HCP_nonTwin(self, main_path, n_shuffles=100):
		"""
		UKB: sample N = HCP/nonTwin cohort 
		"""
		# load existing sampling 
		ipath = f'{main_path}_UKB/twas_repl_samples_HCPnonTwin.hdf5'
		with h5py.File(ipath, 'r') as f: 
			data = f['repl_idx'][()]

		# sample
		UK_SAMPLES = 39565
		FULL_IDXS = np.arange(UK_SAMPLES).astype(int)

		N_NONTWIN = 657
		repl_idxs = np.zeros((n_shuffles, N_NONTWIN), dtype=int)
		for i in range(n_shuffles): 
			idx = np.random.choice(FULL_IDXS, N_NONTWIN, replace=False) 
			repl_idxs[i] = np.sort(idx)

		# concat old and new 
		repl_idxs = np.concatenate((repl_idxs, data), axis=0)
		opath = f'{main_path}_UKB/twas_repl_samples_HCPnonTwin.hdf5'
		with h5py.File(opath, 'w') as f: 
			f['repl_idx'] = repl_idxs


	def sample_UKB_HCP_allEuro(self, main_path, n_shuffles=100):
		"""
		UKB: sample N = HCP/allEuro cohort 
		"""
		# sample
		UK_SAMPLES = 39565
		FULL_IDXS = np.arange(UK_SAMPLES).astype(int)

		N_NONTWIN = 772
		repl_idxs = np.zeros((n_shuffles, N_NONTWIN), dtype=int)
		for i in range(n_shuffles): 
			idx = np.random.choice(FULL_IDXS, N_NONTWIN, replace=False) 
			repl_idxs[i] = np.sort(idx)

		opath = f'{main_path}_UKB/twas_repl_samples_HCPallEuro.hdf5'
		with h5py.File(opath, 'w') as f: 
			f['repl_idx'] = repl_idxs


	def run(self):
		main_path = f'{Config.DATA_ROOT}/inputs'

		# TODO - take n_shuffles as input
		n_shuffles = 100

		# self.sample_UKB_HCP_nonTwin(400)
		self.sample_UKB_HCP_allEuro(500, 100)