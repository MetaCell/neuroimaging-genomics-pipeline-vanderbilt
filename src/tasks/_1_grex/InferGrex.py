import sciluigi as sl
import os
import subprocess
from multiprocessing import Pool

from src.config.Config import Config
from src.tasks._1_grex.convert_to_dosage import ConvertGenotypeProbabilitiesTask


class RunImputationModelsTask(sl.Task):
    """
    A sciluigi task to run imputation models for brain tissues that pass prediction quality thresholds.
    """
    group = sl.Parameter()
    model = sl.Parameter()
    basepath = sl.Parameter()
    done = False

    def out_grex(self):
        return sl.TargetInfo(self, f'{self.basepath}/inputs_{self.group}/grex_{self.model}')

    def requires(self):
        return ConvertGenotypeProbabilitiesTask(group=self.group, model=self.model, basepath=self.basepath, workflow_task=self.workflow_task, instance_name='ConvertGenotypeProbabilitiesTask')
    
    def run(self):
        group = self.group
        model = self.model

        genotyp = f'{self.basepath}/inputs_{group}/dosage_{model}/c*.dosage.txt'
        samples = f'{Config.DATA_ROOT}/inputs_{group}/cohort.txt'

        grex_script = Config.GREX_SCRIPT_PATH
        short_names = Config.grex_short_names
        model_names = Config.grex_model_names
        models_path = Config.MODEL_TISSUE_DATA_PATH.replace('MODEL_NAME', model)
        outgrex = self.out_grex().path

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
                "python", "-u", grex_script,
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

        self.done = True

    def complete(self):
        if self.done:
            return True
        else:
            return False
        

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