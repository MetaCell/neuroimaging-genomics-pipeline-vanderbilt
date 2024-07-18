import os
import time


class Config:
    # TODO: check if the following works with . as the base path
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
    PREP_SAMPLE = f'{DATA_ROOT}/step_0/inputs_GROUP_NAME/bgen_JTI/c1.sample' ## all chrom sample files should be the same
    PATH_JTI = f'{DATA_ROOT}/step_0/aux_files/snps_keep.txt'
    PATH_COHORT = f'{DATA_ROOT}/step_0/inputs_GROUP_NAME/cohort.txt'
    PATH_BGEN = f'{DATA_ROOT}/step_0/inputs_GROUP_NAME/bgen_JTI'
    OUTPUT_VCF_JTI = f'step_0/inputs_COHO/vcf_JTI'


    # STEP-1 - GREX stage-1
    GROUP = 'HCP'
    MODEL = 'JTI'
    VCF_PATH = f'{DATA_ROOT}/step_1/inputs_GROUP_NAME/vcf_MODEL_NAME'
    GREX_DOSAGE_CONVERT_OUTPUT = f'step_1/inputs_GROUP_NAME/dosage_MODEL_NAME'
    GREX_INFER_OUTPUT = f'step_1/inputs_GROUP_NAME/grex_MODEL_NAME'

    # ----------------------------------------------------------------- 

    #STEP-1 - GREX stage-2
    GREX_GENOTYPE_DOSAGE_FORMAT = 'c*.dosage.txt'
    SAMPLE_COHORT_PATH = f'{DATA_ROOT}/step_1/inputs_GROUP_NAME/cohort.txt'
    GREX_SCRIPT_PATH = f'{PROJECT_BASE_PATH}/software/MetaXcan/software/Predict.py'
    MODEL_TISSUE_DATA_PATH = f'{DATA_ROOT}/step_1/aux_files/models_MODEL_NAME/models_by_tissue'  ## do not edit MODEL_NAME - it will be replaced by the model name in the code
    GENOTYPE_INPUT = f'step_1/inputs_GROUP_NAME/dosage_MODEL_NAME/{GREX_GENOTYPE_DOSAGE_FORMAT}'
    
    # ensure the files inside the models_by_tissue consist of the following files
    grex_short_names = ["hippocampus", "amygdala", "caudate", "nucleus-accumbens", "putamen",
                    "cerebellar-hemisphere", "anterior-cingulate", "dlpfc"]
    grex_model_names = ["Hippocampus", "Amygdala", "Caudate_basal_ganglia",
                    "Nucleus_accumbens_basal_ganglia", "Putamen_basal_ganglia",
                    "Cerebellar_Hemisphere", "Anterior_cingulate_cortex_BA24", "Frontal_Cortex_BA9"]


    OUTPUT_HDF5_TO_STEP_2_INPUT = f'{DATA_ROOT}/step_2/inputs_GROUP_NAME/'

    # STEP-2 - TWAS - stage-1
    COHORT = 'UKB'   ## UKB/twas_JTI/vol_mean
    TWAS_WHICH = 'same'
    TWAS_PHENS = 'connmean_noGS_mean'
    BRAIN_NAMES = grex_short_names
    COVS = ['age', 'isMale']


    # STEP-3 GWAS 



    # STEP-4 WEBG



    # STEP-5 - POLY




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