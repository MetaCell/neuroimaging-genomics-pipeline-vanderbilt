import sciluigi as sl
import os
import subprocess
from multiprocessing import Pool

from src.config.Config import Config
from src.tasks.grex.convert_to_dosage import ConvertGenotypeProbabilitiesTask


class RunImputationModelsTask(sl.Task):
    """
    A sciluigi task to run imputation models for brain tissues that pass prediction quality thresholds.
    """
    group = sl.Parameter()
    model = sl.Parameter()
    basepath = sl.Parameter()

    def out_grex(self):
        # Define the output target for GREx path
        return sl.TargetInfo(self, f'{self.basepath}/inputs_{self.group}/grex_{self.model}')

    def requires(self):
        return ConvertGenotypeProbabilitiesTask()

    def run(self):
        group = self.group
        model = self.model

        genotyp = f'{self.basepath}/inputs_{group}/dosage_{model}/c*.dosage.txt'
        samples = f'{Config.DATA_ROOT}/inputs_{group}/cohort.txt'

        # TODO Can be moved to config
        grex_script = Config.GREX_SCRIPT_PATH
        models_path = f'{Config.DATA_ROOT}/aux_files/models_{model}/models_by_tissue'
        outgrex = self.out_grex().path

        short_names = ["hippocampus", "amygdala", "caudate", "nucleus-accumbens", "putamen",
                       "cerebellar-hemisphere", "anterior-cingulate", "dlpfc"]
        model_names = ["Hippocampus", "Amygdala", "Caudate_basal_ganglia",
                       "Nucleus_accumbens_basal_ganglia", "Putamen_basal_ganglia",
                       "Cerebellar_Hemisphere", "Anterior_cingulate_cortex_BA24", "Frontal_Cortex_BA9"]

        # Ensure output directory exists
        if not os.path.exists(outgrex):
            os.makedirs(outgrex)

        log_dir = os.path.join(outgrex, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        for idx in range(len(short_names)):
            print(f"- {short_names[idx]} -")
            model_db_path = os.path.join(models_path, f'{model}_Brain_{model_names[idx]}.db')
            output_path = os.path.join(outgrex, f'{short_names[idx]}.hdf5')
            log_path = os.path.join(log_dir, f'{short_names[idx]}.log')

            cmd = [
                "/home/alxbrd/anaconda3/envs/bg/bin/python", "-u", grex_script,
                "--model_db_path", model_db_path,
                "--text_genotypes", genotyp,
                "--text_sample_ids", samples,
                "--prediction_output", output_path,
                "HDF5",
                "--prediction_summary_output", log_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
            print(result.stderr)

if __name__ == '__main__':
    class Workflow(sl.WorkflowTask):
        group = sl.Parameter()
        model = sl.Parameter()
        basepath = sl.Parameter()

        def workflow(self):
            run_imputation_task = self.new_task('run_imputation_models', RunImputationModelsTask,
                                                group=self.group, model=self.model, basepath=self.basepath)
            return run_imputation_task

    sl.run_local(main_task_cls=Workflow)