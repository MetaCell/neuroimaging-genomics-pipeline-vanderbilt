#!/bin/bash

ipath="/data1/rubinov_lab/brain_genomics/paper_twas/inputs_UKB"
cpath="${ipath}/gwas_covariates.txt"
ppath="${ipath}/phenotypes/gwas_cort_vol_mean.txt" 

#for CHR in {22..2} 
#do 
#    ./regenie \
#        --step 1 \
#        --bgen ../genotype_prepro/chr_bgen_final/c${CHR}.bgen \
#        --covarFile ${cpath} \
#        --phenoFile ${ppath} \
#        --bsize 1000 \
#        --lowmem \
#        --lowmem-prefix mem_tmp_c${CHR} \
#        --threads 1 \
#        --out c${CHR} & 
#done 
#
#./regenie \
#    --step 1 \
#    --bgen ../genotype_prepro/chr_bgen_final/c1.bgen \
#    --covarFile ${cpath} \
#    --phenoFile ${ppath} \
#    --bsize 1000 \
#    --lowmem \
#    --lowmem-prefix mem_tmp_c1 \
#    --threads 1 \
#    --out c1  

for CHR in {22..1} 
do

    if [ ! -e c${CHR}_pred.list ]; then
        continue 
    fi

    ./regenie \
        --step 2 \
        --bgen ../genotype_prepro/chr_bgen_final/c${CHR}.bgen \
        --ref-first \
        --sample ../genotype_prepro/chr_bgen_final/c1.sample \
        --covarFile ${cpath} \
        --phenoFile ${ppath} \
        --pred c${CHR}_pred.list \
        --bsize 1000 \
        --threads 1 \
        --out nh_feb2024_s2_output/c${CHR} & 
done

