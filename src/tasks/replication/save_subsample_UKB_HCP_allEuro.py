import numpy as np 
import h5py  

from src.config.Config import Config
import sciluigi as sl
from src.utils.filesystem import create_path_if_not_exists


class SaveSubsamplesTask(sl.Task):
	"""
	Save random subsample indices for the UKB data. 
	"""
	done = False
	basepath = sl.Parameter()
	nshuffles = sl.Parameter()

	def out_subsamples(self):
		# Output target for subsamples path
		return sl.TargetInfo(self, f'{self.basepath}/{Config.REPLICATION_OUTPATH}/')


	def requires(self):
		pass

	def sample_UKB_HCP_allEuro(self):
		"""
		UKB: sample N = HCP/allEuro cohort 
		"""
		nshuffles = int(self.nshuffles)
		# sample
		UK_SAMPLES = 39565
		FULL_IDXS = np.arange(UK_SAMPLES).astype(int)

		N_NONTWIN = 772
		repl_idxs = np.zeros((nshuffles, N_NONTWIN), dtype=int)
		for i in range(nshuffles): 
			idx = np.random.choice(FULL_IDXS, N_NONTWIN, replace=False) 
			repl_idxs[i] = np.sort(idx)

		opath = str(self.out_subsamples().path)
		create_path_if_not_exists(opath)
		opath_hdf5 = f'{opath}/twas_repl_samples_HCPallEuro.hdf5'

		with h5py.File(opath_hdf5, 'w') as f: 
			f['repl_idx'] = repl_idxs


	def run(self):
		self.sample_UKB_HCP_allEuro()
		self.done = True

	def complete(self):
		return self.done

if __name__ == '__main__':
	class Workflow(sl.WorkflowTask):
		basepath = sl.Parameter()
		nshuffles = sl.Parameter()

		def workflow(self):
			run_save_subsample = self.new_task('run_save_subsample', SaveSubsamplesTask, basepath=self.basepath, nshuffles=self.nshuffles)
			return run_save_subsample

		
	sl.run_local(main_task_cls=Workflow)
