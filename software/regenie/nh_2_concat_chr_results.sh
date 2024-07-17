#!/bin/bash

# Concat regenie chr results into one file. 
# Nhung, April 2023 

regs=(amygdala caudate cerebellar-hemisphere hippocampus nucleus-accumbens putamen anterior-cingulate frontal-pole prefrontal-cortex)
regs=(anterior-cingulate dlpfc)

for REG in ${regs[*]}
do
    cp nh_feb2024_s2_output/c1_${REG}.regenie nh_feb2024_gwas/vol_mean_${REG}.regenie 
    echo ${REG}

    for CHR in {2..22} 
    do 
        tail -n +2 nh_feb2024_s2_output/c${CHR}_${REG}.regenie >> nh_feb2024_gwas/vol_mean_${REG}.regenie        
        echo ${CHR}
    done 
done
