import os
import time


class Config:

    #General Parameters
    OUTPUT_BASEPATH = '/home/alxbrd/projects/metacell/vanderbilt/brain_genomics_metacell/output/'

    DATA_ROOT = '/home/alxbrd/projects/metacell/vanderbilt/brain_genomics_metacell/data'
    PLINK_PATH = '/home/alxbrd/projects/metacell/vanderbilt/brain_genomics_metacell/plink/plink2'
    BGENIX_PATH = '/home/alxbrd/projects/metacell/vanderbilt/brain_genomics_metacell/bgenix/bgenix'

    # Prep Step 0
    SAMPLE = f'{DATA_ROOT}/step_0/0_bgen_JTI/c1.sample' ## all chrom sample files should be the same
    BGEN_ROOT = f'{DATA_ROOT}/step_0/0_bgen_JTI/'

    # GREX Step 1
    GROUP = 'HCP'
    MODEL = 'JTI'

    #GREX Step 2
    GREX_SCRIPT_PATH = f'{DATA_ROOT}/aux_scripts/MetaXcan/software/Predict.py'

    # TWAS Step 1
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