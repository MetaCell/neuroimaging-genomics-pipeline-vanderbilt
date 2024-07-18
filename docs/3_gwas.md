
### Step 3: GWAS
<hr />

#### 3.1. Format Phenotypes and Covariates
`INPUT`
We need the  files in the following structure:
--cohort_path
```bash
data/step_3/inputs_GROUP_NAME/cohort.txt
```

--phenotype_path
```bash
data/step_3/inputs_GROUP_NAME/phenotypes/vol_mean.csv
```

--covariate_path
```bash
data/step_3/inputs_GROUP_NAME/covariates.csv
```




`OUTPUT`
output can be seen in 
--phen_out_path && --cov_out_path
```bash
output/step_3/inputs_GROUP_NAME/phenotypes/gwas_vol_mean.txt
output/step_3/inputs_GROUP_NAME/gwas_covariates.txt
```



#### 3.2. Get QC Stats
`INPUT`

--bgen_raw
below chr_num is a number between 1-22
```bash
data/step_3/inputs_GROUP_NAME/bgen_raw/c{chr_num}.bgen
```

--sample_path
below chr_num is a number between 1-22
```bash
data/step_3/inputs_GROUP_NAME/bgen_raw/c{chr_num}.sample

```




`OUTPUT`
output can be seen in 
```bash
'output/step_3/bgen_JTI/*'
```


#### 3.3 Run Regenie

`INPUT`
--ipath - coming from output of previous step - can be seen at `output/step_3/inputs_GROUP_NAME/bgen_JTI` 
--cpath - `data/step_3/inputs_GROUP_NAME/gwas_covariates.txt`
--ppath - `data/step_3/inputs_GROUP_NAME/phenotypes/gwas_vol_mean.txt`


`OUTPUT`
```bash
output/step_3/outputs_GROUP_NAME/gwas/*



#### 3.4 Concat CHR results


`INPUT`
taken from the output of the previous step - run regenie
`output/step_3/outputs_GROUP_NAME/gwas/*`


`OUTPUT`
Concatenates into files like `vol_mean_amygdala.regenie`. Output is at the same folder location at:
`output/step_3/outputs_GROUP_NAME/gwas/*`



#### 3.5 Compare GWAS and TWAS

`INPUT`



`OUTPUT`


















## How to run GWAS pipeline
<hr />

1. To run the format_phens_and_covs
```bash
python -m src.tasks._3_gwas.format_phens_and_covs --basepath ./output --group UKB
```

2. To run the get_QC_stats
```bash
python -m src.tasks._3_gwas.get_QC_stats --basepath ./output --group UKB
```

3. To run the run_regenie 
```bash
python -m src.tasks._3_gwas.run_regenie --basepath ./output --group UKB
```

4. To run the concat_chr_results 
```bash
python -m src.tasks._3_gwas.concat_chr_results --basepath ./output --group UKB
```

5. To run the compare_gwas_twas
```bash
python -m src.tasks._3_gwas.compare_gwas_twas --basepath ./output --group UKB --phens vol_mean
```



