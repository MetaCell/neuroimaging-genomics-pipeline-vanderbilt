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

	def sample_UKB(self):
		nshuffles = int(self.nshuffles)
		UK_SAMPLES = 39565
		FULL_IDXS = np.arange(UK_SAMPLES).astype(int)
		opath = str(self.out_subsamples().path)
		create_path_if_not_exists(opath)
		opath_hdf5 = f'{opath}/twas_repl_samples.hdf5'


		samp_idxs = {}
		disc_sizes = [772, 2000, 5000, 15000]

		for dsc in disc_sizes:

			ds = UK_SAMPLES - dsc

			idxs = np.zeros((nshuffles, ds), dtype=int)
			for i in range(nshuffles):
				idx = np.random.choice(FULL_IDXS, ds, replace=False)
				idxs[i] = np.sort(idx)

			samp_idxs[dsc] = idxs
		
		with h5py.File(opath_hdf5, 'w') as f:
			for ds, idxs in samp_idxs.items():
				f[str(ds)] = idxs


	def run(self):
		self.sample_UKB()
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
