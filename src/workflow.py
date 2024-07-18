import sciluigi as sl

from src.config.Config import Config
from src.tasks._1_grex.infer_grex import RunImputationModelsTask
from src.tasks._1_grex.convert_to_dosage import ConvertGenotypeProbabilitiesTask
from src.tasks._2_twas.run_twas import RunTwasTask
from src.tasks._2_twas.clean_twas import CleanTwasTask
from src.tasks._2_twas.concat_twas import ConcatTwasTask
from src.tasks._2_twas.count_pdx_overlap import CountPDXOverlapTask


class Workflow(sl.WorkflowTask):

    workflow_instance = Config.create_output_timestamp_dir()

    def workflow(self):
        run_instance = self.workflow_instance

        # STEP-1
        convert_task = self.new_task('convert_genotype_probabilities', ConvertGenotypeProbabilitiesTask,
                                     group=Config.GROUP, model=Config.MODEL, basepath=run_instance)

        infer_grex = self.new_task('infer_grex', RunImputationModelsTask,
                                     group=Config.GROUP, model=Config.MODEL, basepath=run_instance)

        infer_grex.requires = lambda: convert_task

        # STEP-2
        run_twas = self.new_task('run_twas', RunTwasTask, group=Config.GROUP, model=Config.MODEL, which=Config.TWAS_WHICH, phens=Config.TWAS_PHENS, basepath=run_instance)
        clean_twas = self.new_task('clean_twas', CleanTwasTask, cohort=Config.COHORT, basepath=run_instance)
        concat_twas = self.new_task('concat_twas', ConcatTwasTask, group=Config.GROUP, phens=Config.CONCAT_TWAS_PHENS, basepath=run_instance)
        count_pdx_overlap = self.new_task('count_pdx_overlap', CountPDXOverlapTask, ptype=Config.PTYPE, group=Config.GROUP, basepath=run_instance)

        # define what is required to run each task


        # STEP-3
        



        # Return the last task(s) in the workflow chain.
        return count_pdx_overlap

if __name__ == '__main__':
    sl.run_local(main_task_cls=Workflow)