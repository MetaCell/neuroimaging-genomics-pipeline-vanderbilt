#!/bin/bash

# Concat regenie chr results into one file. 
# Nhung, April 2023 

regs=(amygdala anterior-cingulate caudate cerebellar-hemisphere dlpfc hippocampus nucleus-accumbens putamen)

ipath="../../data/outputs_UKB/gwas"

for REG in ${regs[*]}
do
    cp ${ipath}/s2_c1_${REG}.regenie ${ipath}/vol_mean_${REG}.regenie 
    echo ${REG}

    for CHR in {2..22} 
    do 
        tail -n +2 ${ipath}/s2_c${CHR}_${REG}.regenie >> ${ipath}/vol_mean_${REG}.regenie        
        echo ${CHR}
    done 
done
