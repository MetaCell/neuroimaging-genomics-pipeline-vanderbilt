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

	def sample_HCP(self):
		nshuffles = int(self.nshuffles)
		ALL_EURO = 772
		NON_TWIN = 657
		
		opath = str(self.out_subsamples().path)
		create_path_if_not_exists(opath)
		opath_hdf5 = f'{opath}/twas_repl_samples_HCPnonTwin.hdf5'


		FULL_IDXS = np.arange(39565).astype(int)
		SAMPLE_IDXS = np.zeros((nshuffles, ALL_EURO), dtype=int)
		for i in range(nshuffles):
			idx = np.random.choice(FULL_IDXS, ALL_EURO, replace=False)
			SAMPLE_IDXS[i] = np.sort(idx)

		with h5py.File(opath_hdf5, 'w') as f:
			f['repl_idx'] = SAMPLE_IDXS


	def run(self):
		self.sample_HCP()
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
