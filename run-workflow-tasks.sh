#!/bin/bash

# Define a workflow run output identifier consisting of the current timestamp
CURRENT_TIMESTAMP=$(date +%s)

# Define the workflow run output path which is unique to this run
OUTPUT_FOLDER_NAME="./output/workflow-run-${CURRENT_TIMESTAMP}"
echo "Creating output folder at ${OUTPUT_FOLDER_NAME}..."
mkdir -p OUTPUT_FOLDER_NAME
echo "Folder created successfully."

# Step 0: Prep
python -m src.tasks._0_prep.extra_cohort_snps --coho UKB --basepath $OUTPUT_FOLDER_NAME

# Step 1: Grex
python -m src.tasks._1_grex.convert_to_dosage --group UKB --model JTI --basepath $OUTPUT_FOLDER_NAME
python -m src.tasks._1_grex.infer_grex --group UKB --model JTI --basepath $OUTPUT_FOLDER_NAME

# Step 2: TWAS
python -m src.tasks._2_twas.run_twas --group UKB --model JTI --basepath $OUTPUT_FOLDER_NAME --which same --phens vol_mean
#python -m src.tasks._2_twas.run_twas --group UKB --model JTI --basepath $OUTPUT_FOLDER_NAME --which same --phens connmean_noGS_mean

python -m src.tasks._2_twas.clean_twas --cohort UKB --basepath $OUTPUT_FOLDER_NAME
python -m src.tasks._2_twas.concat_twas --group UKB --phens vol_mean --basepath $OUTPUT_FOLDER_NAME
python -m src.tasks._2_twas.count_pdx_overlap --ptype FDR --group UKB --basepath $OUTPUT_FOLDER_NAME

# Step 3: GWAS
python -m src.tasks._3_gwas.format_phens_and_covs --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._3_gwas.get_QC_stats --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._3_gwas.run_regenie --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._3_gwas.concat_chr_results --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._3_gwas.compare_gwas_twas --basepath $OUTPUT_FOLDER_NAME --group UKB --phens vol_mean

# Step 4: WEBG
python -m src.tasks._4_webg.save_predixvu_gmt  --basepath $OUTPUT_FOLDER_NAME
python -m src.tasks._4_webg.save_interest_sets  --basepath $OUTPUT_FOLDER_NAME --group UKB --phens vol_mean --ptype FDR
python -m src.tasks._4_webg.run_webgestalt  --basepath $OUTPUT_FOLDER_NAME --group UKB --phens vol_mean --ptype FDR --ontol pdx_nom0.001
python -m src.tasks._4_webg.save_enrich_summary  --basepath $OUTPUT_FOLDER_NAME --group UKB --phens vol_mean --enrich pdx_nom0.001 --ptype FDR

# Step 5: POLY
python -m src.tasks._5_poly.regress_phen  --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._5_poly.poly_stats  --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._5_poly.poly_perm_stats  --basepath $OUTPUT_FOLDER_NAME --group UKB
python -m src.tasks._5_poly.twas_stats  --basepath $OUTPUT_FOLDER_NAME --group UKB