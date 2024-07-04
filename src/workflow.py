import sciluigi as sl

from src.config.Config import Config
from src.tasks.grex.InferGrex import RunImputationModelsTask
from src.tasks.grex.convert_to_dosage import ConvertGenotypeProbabilitiesTask


class Workflow(sl.WorkflowTask):

    workflow_instance = Config.create_output_timestamp_dir()

    def workflow(self):
        run_instance = self.workflow_instance

        convert_task = self.new_task('convert_genotype_probabilities', ConvertGenotypeProbabilitiesTask,
                                     group=Config.GROUP, model=Config.MODEL, basepath=run_instance)

        infer_grex = self.new_task('infer_grex', RunImputationModelsTask,
                                     group=Config.GROUP, model=Config.MODEL, basepath=run_instance)

        infer_grex.requires = lambda: convert_task

        # Return the last task(s) in the workflow chain.
        return infer_grex

if __name__ == '__main__':
    sl.run_local(main_task_cls=Workflow)