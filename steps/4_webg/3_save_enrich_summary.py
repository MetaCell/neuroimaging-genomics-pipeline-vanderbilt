'''
Save a summary table of the enrichment results. 

- Nhung, updated June 2024
'''

import pandas as pd 
import sys 

enric = sys.argv[1] ## pdx_nom0.001
phens = sys.argv[2] ## FDR_vol_mean_interreg

# top_path = '/data1/rubinov_lab/brain_genomics/metacell' 
top_path = '../../data'

enr_path = f'{top_path}/outputs_UKB/enrich_{enric}/{phens}/enrichment_results' ## _{reg}.txt 
out_path = f'{top_path}/outputs_UKB/enrich_{enric}/{phens}/enrichment_summary.csv'

cols = ['geneSet', 'description', 'size', 'overlap', 'enrichmentRatio', 'pValue', 'FDR']
name = ['annotation', 'description', 'num annot genes', \
        'pheno-annot overlap', 'enrichment ratio', 'pvalue', 'FDR']
cdict = {c: n for c, n in zip(cols, name)}

regs = ['dlpfc', 'anterior_cingulate', 'amygdala', 'hippocampus', \
        'caudate', 'putamen', 'nucleus_accumbens', 'cerebellar_hemisphere']

summ = None
for reg in regs:

    df = pd.read_table(f'{enr_path}_{reg}.txt', usecols=cols).rename(columns=cdict)

    ## temp bandaid
    if enric == 'gwas_catalog': 
        df['annotation'] = df['annotation'].apply(lambda x: x.split(' | ')[0])
        df['description'] = df['description'].apply(lambda x: x.split(' | ')[1])
    ##

    df.insert(3, 'twas phenotype', reg)

    if summ is None: summ = df
    else: summ = pd.concat([summ, df])

summ.to_csv(out_path, index=False)
