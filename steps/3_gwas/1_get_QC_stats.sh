#! /bin/bash

## Clean up raw genotype files for GWAS

MAIN="/data1/rubinov_lab/brain_genomics/metacell/metacell2/inputs_UKB"

for CHR in {22..1}
do 
    ## save new chr files with hard call genotypes  
    plink2 --bgen ${MAIN}/bgen_raw/c${CHR}.bgen ref-first \
           --sample ${MAIN}/bgen_raw/c${CHR}.sample \
           --snps-only \
           --hard-call-threshold 0.1 \
           --make-pgen \
           --out ${MAIN}/bgen_JTI/c${CHR} 

    ## apply filters for missingness, then MAF 
    plink2 --pfile ${MAIN}/bgen_JTI/c${CHR} \
           --geno 0.05 \
           --maf 0.01 \
           --make-pgen \
           --out ${MAIN}/bgen_JTI/c${CHR} 

    ## remove duplicate SNPs (by id, keep one), then apply HWE filter 
    ## export as bgen
    plink2 --pfile ${MAIN}/bgen_JTI/c${CHR} \
           --rm-dup exclude-mismatch \
           --hwe 0.00001 \
           --export bgen-1.2 'bits=8' \
           --out ${MAIN}/bgen_JTI/c${CHR}

    ## index bgen file 
    bgenix -g ${MAIN}/bgen_JTI/c${CHR}.bgen -index -clobber & 

    ## sanity check 
    #plink2 --bgen ${MAIN}/bgen_JTI/c${CHR}.bgen ref-first \
    #       --sample ${MAIN}/bgen_JTI/c${CHR}.sample \
    #       --freq \
    #       --out c${CHR} &
done 
