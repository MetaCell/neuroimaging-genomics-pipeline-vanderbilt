import os
import time


class Config:
    PROJECT_BASE_PATH = '/home/dgk/metacell/brain_genomics/VANDERBILT/neuroimaging-genomics-pipeline-vanderbilt'
    
    #General Parameters
    OUTPUT_BASEPATH = f'{PROJECT_BASE_PATH}/output/'

    DATA_ROOT = f'{PROJECT_BASE_PATH}/data'

    # Software Paths
    PLINK_PATH = None          ## if you want to provide a specific path to plink, provide it here
    BGENIX_PATH = f'{PROJECT_BASE_PATH}/software/bgenix/bgenix'
    METAXCAN_PATH = f'{PROJECT_BASE_PATH}/software/MetaXcan'
    REGENIE_PATH = f'{PROJECT_BASE_PATH}/software/regenie'

    # STEP-0 - Prep 
    SAMPLE = f'{DATA_ROOT}/step_0/0_bgen_JTI/c1.sample' ## all chrom sample files should be the same
    BGEN_ROOT = f'{DATA_ROOT}/step_0/0_bgen_JTI/'


    # STEP-1 - GREX stage-1
    GROUP = 'HCP'
    MODEL = 'JTI'

    #STEP-1 - GREX stage-2
    GREX_SCRIPT_PATH = f'{PROJECT_BASE_PATH}/software/MetaXcan/software/Predict.py'
    MODEL_TISSUE_DATA_PATH = f'{DATA_ROOT}/aux_files/models_MODEL_NAME/models_by_tissue'  ## do not edit MODEL_NAME - it will be replaced by the model name in the code
    
    # ensure the files inside the models_by_tissue consist of the following files
    grex_short_names = ["hippocampus", "amygdala", "caudate", "nucleus-accumbens", "putamen",
                    "cerebellar-hemisphere", "anterior-cingulate", "dlpfc"]
    grex_model_names = ["Hippocampus", "Amygdala", "Caudate_basal_ganglia",
                    "Nucleus_accumbens_basal_ganglia", "Putamen_basal_ganglia",
                    "Cerebellar_Hemisphere", "Anterior_cingulate_cortex_BA24", "Frontal_Cortex_BA9"]



    # STEP-2 - TWAS - stage-1
    COHORT = ''

    @staticmethod
    def create_output_timestamp_dir():
        # Get the current Unix timestamp
        timestamp = int(time.time())

        # Create the directory path
        dir_path = os.path.join(Config.OUTPUT_BASEPATH, str(timestamp))

        # Create the directory
        os.makedirs(dir_path, exist_ok=True)

        # Return the full path of the created directory
        return dir_path