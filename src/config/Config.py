import os
import time


class Config:
    # TODO: check if the following works with . as the base path
    PROJECT_BASE_PATH = os.getenv('BASE_PATH', './')
    
    #General Parameters
    OUTPUT_BASEPATH = f'{PROJECT_BASE_PATH}/output/'

    DATA_ROOT = f'{PROJECT_BASE_PATH}/data'

    # Software Paths
    PLINK_PATH = os.getenv('PLINK_PATH', f'{PROJECT_BASE_PATH}/software/plink2')          ## if you want to provide a specific path to plink, provide it here
    BGENIX_PATH = os.getenv('BGENIX_PATH', f'{PROJECT_BASE_PATH}/software/bgenix/bgenix')

    METAXCAN_PATH = f'{PROJECT_BASE_PATH}/software/MetaXcan'
    REGENIE_PATH = f'{PROJECT_BASE_PATH}/software/regenie/regenie'

    # STEP-0 - Prep 
    PREP_SAMPLE = f'{DATA_ROOT}/step_0/inputs_GROUP_NAME/bgen_JTI/c1.sample' ## all chrom sample files should be the same
    PATH_JTI = f'{DATA_ROOT}/step_0/aux_files/snps_keep.txt'
    PATH_COHORT = f'{DATA_ROOT}/step_0/inputs_GROUP_NAME/cohort.txt'
    PATH_BGEN = f'{DATA_ROOT}/step_0/inputs_GROUP_NAME/bgen_JTI'
    OUTPUT_VCF_JTI = f'step_0/inputs_COHO/vcf_JTI'


    # STEP-1 - GREX stage-1
    GROUP = 'UKB'
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


    # ----------------------------------------------------------------- 
    # STEP-2 - TWAS 
    COHORT = 'UKB'   ## UKB/twas_JTI/vol_mean
    TWAS_WHICH = 'same'
    TWAS_PHENS = 'connmean_noGS_mean'
    BRAIN_NAMES = grex_short_names
    COVS = ['age', 'isMale']

    TWAS_SCRIPT = f'{METAXCAN_PATH}/software/PrediXcanAssociation.py'

    GREX_JTI_OUTPUT_PATH=f"step_1/inputs_GROUP_NAME/grex_MODEL_NAME"
    PHEN_FILE=f"{DATA_ROOT}/step_2/inputs_GROUP_NAME/phenotypes/TWAS_PHENS.csv"
    COVS_FILE=f"{DATA_ROOT}/step_2/inputs_GROUP_NAME/covariates.csv"
    TWAS_RUN_OUTPUT_PATH = f'step_2/outputs_GROUP_NAME/twas_MODEL_NAME'
    CONCAT_TWAS_OUTPUT_PATH = f'step_2/outputs_GROUP_NAME/twas_JTI'
    COUNT_PDX_OVERLAP_PATH = f'step_2/outputs_GROUP_NAME/pdx_overlap'

    # concat twas
    CONCAT_TWAS_PHENS = 'vol_mean'
    TWAS_REGS = grex_short_names
    PTYPE = 'FDR'
    TWAS_PATH = f'{DATA_ROOT}/step_2/outputs_GROUP_NAME/twas_JTI/PHENS'
    ITWA_PATH = f'{DATA_ROOT}/step_2/outputs_GROUP_NAME/twas_JTI/cross_regs/PHENS'
    GENE_PATH = f'{DATA_ROOT}/step_2/aux_files/models_JTI/syms_by_tissue/jti_ens_to_sym.csv'
    OUTS_PATH = f'{DATA_ROOT}/step_2/outputs_GROUP_NAME/twas_JTI/summary.csv'

    TWAS_COLUMN_NAMES = ['sym', 'ens', 'grex', 'phen', 'beta', 'pval', 'FDR', 'BON']


    # count pdx overlap
    SYM_PATH = f'{DATA_ROOT}/step_2/aux_files/models_JTI/syms_by_tissue/jti_ens_to_sym.csv'
    PHE_PATH = f'{DATA_ROOT}/step_2/aux_files/predixvu_phenames.csv'
    PDX_PATH = f'{DATA_ROOT}/step_2/aux_files/predixvu_assocs.csv.gz'
    TWA_PATH = f'{DATA_ROOT}/step_2/outputs_GROUP_NAME/twas_JTI/summary.csv'
    MOD_NAMES = grex_model_names
    REG_NAMES = grex_short_names

    # ----------------------------------------------------------------- 

    # STEP-3 GWAS 

    COHORT_PATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME/cohort.txt'
    PHEN_PATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME/phenotypes/vol_mean.csv'
    COVS_PATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME/covariates.csv'

    GWAS_FORMAT_OUT_PATH = f'step_3/inputs_GROUP_NAME/'
    PHEN_OUT_PATH = f'phenotypes/gwas_vol_mean.txt' 
    COVS_OUT_PATH = f'gwas_covariates.txt' 

    # get QC stats
    GWAS_QC_OUT_PATH = f'step_3/inputs_GROUP_NAME/bgen_JTI'
    # bgen_raw = f'{Config.DATA_ROOT}/bgen_raw/c{chr_num}.bgen ref-first'
    # sample_path = f'{Config.DATA_ROOT}/bgen_raw/c{chr_num}.sample'
    BGEN_RAW_PATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME/bgen_raw'

    GWAS_IPATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME'
    GWAS_IPATH_FROM_OUTPUT_PATH = f'step_3/inputs_GROUP_NAME/bgen_JTI'
    GWAS_CPATH = f'{GWAS_IPATH}/gwas_covariates.txt'
    GWAS_PPATH = f'{GWAS_IPATH}/phenotypes/gwas_vol_mean.txt'
    GWAS_BGEN_FILES_PATH = f'step_3/inputs_GROUP_NAME/bgen_JTI'
    GWAS_RUN_REGENIE_OUTPUT_PATH = f'step_3/outputs_GROUP_NAME/gwas'
    GWAS_REGS = grex_short_names

    # Compare GWAS TWAS
    WJTI_PATH = f'{DATA_ROOT}/step_3/aux_files/models_JTI/weights_by_tissue'
    COMPARE_TWAS_PATH = f'step_2/outputs_GROUP_NAME/twas_JTI/PHENS'
    COMPARE_GWAS_PATH = f'step_3/outputs_GROUP_NAME/gwas/PHENS'

    SUMM_PATH = f'step_3/outputs_GROUP_NAME/TWAS_GWAS_summary.csv'
    SIG_PATH = f'step_3/outputs_GROUP_NAME/TWAS_GWAS_sigbars.csv'

    SUMM_RTMP = f'step_3/outputs_GROUP_NAME/tgwa'
    SIGS_RTMP = f'step_3/outputs_GROUP_NAME/sigs'



    # ----------------------------------------------------------------- 

    # STEP-4 WEBG
    PHE_RM = [290.2, 290.3, 306.0, 339.0, 346.0, 346.1, 346.2, 348.0, 348.9, 349.0]
    BRN_RM = ['Hypothalamus', 'Substantia_nigra', 'Spinal_cord_cervical_c-1']
    WEBG_PDX_PATH = f'{DATA_ROOT}/step_4/aux_files/predixvu_assocs.csv.gz'
    WEBG_PHE_PATH = f'{DATA_ROOT}/step_4/aux_files/predixvu_brain_phecodes.csv'
    WEBG_PREDIXVU_OUTPUT_PATH = f'step_4/aux_files'

    # save interest sets
    WEBG_REGS = grex_short_names

    # the following are already present fromm the step-2 so we reuse it. 
    WEBG_TWAS_PATH = f'{DATA_ROOT}/step_2/outputs_GROUP_NAME/twas_JTI/PHENS'
    WEBG_ITWA_PATH = f'{DATA_ROOT}/step_2/outputs_GROUP_NAME/twas_JTI/cross_regs/PHENS'
    WEBG_INTEREST_SETS_OUTPUT_PATH = f'step_4/inputs_GROUP_NAME/enrich_sets'

    # ----------------------------------------------------------------- 
    # run webgestalt
    GMT_PATH = f'step_4/aux_files/ONTOL.gmt'
    DES_PATH =  f'step_4/aux_files/ONTOL.des'
    WEBG_JTI_PATH = f'{DATA_ROOT}/step_4/aux_files/models_JTI/genes_by_tissue/'

    WEBG_INN_PATH = f'step_4/inputs_GROUP_NAME/enrich_sets/PTYPE_PHENS_'
    WEBG_OUT_PATH = f'step_4/outputs_GROUP_NAME/enrich_ONTOL/PTYPE_PHENS'


    INSTALL_WEBGESTALT_PATH = f'{PROJECT_BASE_PATH}/src/tasks/_4_webg/install_webgestalt.r'
    RUN_WEBGESTALT_PATH = f'{PROJECT_BASE_PATH}/src/tasks/_4_webg/run_webgestalt.r'

    # enrich summary
    ENR_PATH = f'step_4/outputs_GROUP_NAME/enrich_ENRICH_NAME/PTYPE_PHENS_interreg/enrichment_results' ## _{reg}.txt 
    ENR_OUT_PATH = f'step_4/outputs_GROUP_NAME/enrich_ENRICH_NAME/PTYPE_PHENS_interreg/enrichment_summary.csv'
    ENRICH_SUMMARY_REGS = ['dlpfc', 'anterior_cingulate', 'amygdala', 'hippocampus', \
        'caudate', 'putamen', 'nucleus_accumbens', 'cerebellar_hemisphere']   ## similar to grex_short_names


    # ----------------------------------------------------------------- 

    # STEP-5 - POLY
    COMMON_PHENS = ['vol_mean', 'alff_mean', 'reho_noGS_mean', 'connmean_noGS_mean']

    POLY_COVS_PATH = COVS_PATH    ## already from step-3
    REGRESS_PHEN_PATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME/phenotypes/PHEN_TYPE.csv'      ## phen - already from step-3

    REGRESS_OUT_DIR = f'step_5/outputs_GROUP_NAME/phenotypes'
    REGRESS_OUTS_FILE = f'PHEN_TYPE_regr.csv' ## phen 
    
    # poly_stat

    POLY_SUBJ_PATH = f'{DATA_ROOT}/step_3/inputs_GROUP_NAME/cohort.txt' ## from step 3
    POLY_FAMS_PATH = f'{DATA_ROOT}/step_5/inputs_GROUP_NAME/demographics.csv' 

    POLY_TWAS_PATH = f'step_2/outputs_GROUP_NAME/twas_JTI/PHEN_TYPE/REGION_NAME.txt' ## group, phen, reg - from step-2 output
    POLY_GREX_PATH = f'step_1/inputs_GROUP_NAME/grex_JTI/REGION_NAME.hdf5' ## group, reg - from step-1 output
    POLY_PHEN_PATH = f'step_5/outputs_GROUP_NAME/phenotypes/PHEN_TYPE_regr.csv' ## group, phen - step-5 prev output

    POLY_STATS_OUTPUT_PATH = f'step_5/outputs_GROUP_NAME/polygenic_models'
    A_FILE_PATH = f'{POLY_STATS_OUTPUT_PATH}/median_ytrue_ypred.hdf5'
    B_FILE_PATH = f'{POLY_STATS_OUTPUT_PATH}/split_r2s.hdf5'
    C_FILE_PATH = f'{POLY_STATS_OUTPUT_PATH}/split_pvs.hdf5'

    # poly perm stats
    POLYPERM_SUBJ_PATH = POLY_SUBJ_PATH    ## from step 3
    POLYPERM_FAMS_PATH = POLY_FAMS_PATH    ## from previous script

    POLYPERM_TWAS_PATH = POLY_TWAS_PATH    ## group, phen, reg
    POLYPERM_GREX_PATH = POLY_GREX_PATH    ## group, reg
    POLYPERM_PHEN_PATH = POLY_PHEN_PATH    ## group, phen

    POLYPERM_NTMP_PATH = f'{POLY_STATS_OUTPUT_PATH}/null_tmp' ## /phen_reg_itr.hdf5
    POLYPERM_NULL_PATH = f'{POLY_STATS_OUTPUT_PATH}/nulls.hdf5' ## keys: (reg, phen)

    # twas stats
    # will use the same POLY_TWAS_PATH, POLY_GREX_PATH, and POLY_PHEN_PATH
    TWAS_STATS_OUTPUT_PATH = f'{POLY_STATS_OUTPUT_PATH}/single_stats.hdf5'


    # -----------------------------------------------------------------
    # replication
    REPLICATION_OUTPATH = 'replication'




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