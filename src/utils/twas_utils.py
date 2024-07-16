from statsmodels.stats.multitest import multipletests as sm


## func: FDR correction 
def fcorrect(tdf): 
    tdf['FDR'] = sm(tdf['pval'], method='fdr_bh', alpha=0.05)[1]
    return tdf 

## func: Bonf correction 
def bcorrect(tdf): 
    tdf['BON'] = sm(tdf['pval'], method='bonferroni', alpha=0.05)[1]
    return tdf 