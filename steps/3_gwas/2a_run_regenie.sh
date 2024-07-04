#!/bin/bash

PATH="$PATH:../../data/aux_scripts/regenie"
export PATH

ipath="../../data/inputs_UKB"
cpath="${ipath}/gwas_covariates.txt"
ppath="${ipath}/phenotypes/gwas_vol_mean.txt" 

opath="../../data/outputs_UKB/gwas"

for CHR in {22..2} 
do 
    regenie \
      --step 1 \
      --bgen ${ipath}/bgen_JTI/c${CHR}.bgen \
      --covarFile ${cpath} \
      --phenoFile ${ppath} \
      --bsize 1000 \
      --lowmem \
      --lowmem-prefix mem_tmp_c${CHR} \
      --threads 1 \
      --out c${CHR} & 
done 

regenie \
  --step 1 \
  --bgen ${ipath}/bgen_JTI/c1.bgen \
  --covarFile ${cpath} \
  --phenoFile ${ppath} \
  --bsize 1000 \
  --lowmem \
  --lowmem-prefix mem_tmp_c1 \
  --threads 1 \
  --out c1  

for CHR in {22..1} 
do

    if [ ! -e c${CHR}_pred.list ]; then
        continue 
    fi

    regenie \
      --step 2 \
      --bgen ${ipath}/bgen_JTI/c${CHR}.bgen \
      --ref-first \
      --sample ${ipath}/bgen_JTI/c1.sample \
      --covarFile ${cpath} \
      --phenoFile ${ppath} \
      --pred c${CHR}_pred.list \
      --bsize 1000 \
      --threads 1 \
      --out ${opath}/s2_c${CHR} & 
done

