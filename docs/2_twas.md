
### Step 2: TWAS
<hr />

#### 2.1. Run TWAS 

We need the  files in the following structure:

`INPUT`
1. --hdf5_expression_file: this is list of all the hdf5 files generated from the previous step - in the GREX. You can find all the files at:
```
output/step_1/input_{GROUP_NAME}/grex_{MODEL_NAME}
```

2. --input_phenos_file: Provide with phenotypes. These will contain csv files. The file should be in the following structure:
```
data/step_2/inputs_{GROUP_NAME}/phenotypes/
```

example: 
```
data/step_2/inputs_UKB/phenotypes/vol_mean.csv
```

3. Covariates file: This file should be in the following structure:
```
data/step_2/inputs_{GROUP_NAME}/covariates.csv
```

`OUTPUTS`
```bash
output/step_2/outputs_GROUP_NAME/twas_MODEL_NAME/PHENS/*.txt
```


#### 2.2. Run the clean twas

`INPUT`
To run this we need the data in the format: example of files would be:
['sigs_amygdala.csv', 'sigs_anterior-cingulate.csv', 'tgwa_amygdala.csv', 'tgwa_anterior-cingulate.csv', ...]
```
data/step_2/outputs_{GROUP_NAME}/{file_name}.csv
```

`OUTPUT`
No output, as this replaces the existing files with the cleaned files.



#### 2.3. Concat the twas

`INPUT`
To run this we need the data in the format:

<!-- TODO - The twas_JTI is also a output from previous step. -->
<!-- TODO - are these related and do we want the output of one to be the input of another??? -->
--twas_path
here {PHENS} can be like - vol_mean, etc.
```bash
data/step_2/output_{GROUP_NAME}/twas_{MODEL_NAME}/{PHENS}
```

--itwa_path
```bash
data/step_2/output_{GROUP_NAME}/twas_{MODEL_NAME}/cross_regs/{PHENS}.csv
```

--gene_path
```bash
data/step_2/aux_files/models_JTI/syms_by_tissue/jti_ens_to_sym.csv'
```


`OUTPUT`
This will generate the output file at the following location:

```bash
output/step_2/outputs_{GROUP_NAME}/twas_{MODEL_NAME}/summary.csv
```


#### 2.4. Count the PDX overlap
`INPUT`
--sym_path
```bash
data/step_2/aux_files/models_JTI/syms_by_tissue/jti_ens_to_sym.csv
```

--phe_path
```bash
data/step_2/aux_files/predixvu_phenames.csv
```

--pdx_path
```bash
data/step_2/aux_files/predixvu_assocs.csv.gz
```

--twa_path
this is generated from the previous step, and the summary file is at:
```bash
output/step_2/outputs_GROUP_NAME/twas_JTI/summary.csv
```

`OUTPUT`
This will generate the output file at the following location:
```bash
output/outputs_{GROUP_NAME}/pdx_overlap/{FILE_NAME}.csv
```




## How to run TWAS pipeline

<hr />

1. To execute run_twas, run the following command:

This would have to be run for each phenotype separately - if you have multiple phenotypes, you would have to run this command multiple times. 
Here is the case - for PHENS - connmean_noGS_mean/vol_mean, you would have to run the following command:
```bash
python -m src.tasks._2_twas.run_twas --group UKB --model JTI --basepath ./output --which same --phens vol_mean
```
OR 
```bash
python -m src.tasks._2_twas.run_twas --group UKB --model JTI --basepath ./output --which same --phens connmean_noGS_mean
```

2. To execute clean_twas, run the following command:
cohort can be - UKB/twas_JTI/vol_mean

```bash
python -m src.tasks._2_twas.clean_twas --cohort UKB --basepath ./output
```


3. To execute concat_twas, run the following command:

```bash
python -m src.tasks._2_twas.concat_twas --group UKB --phens vol_mean --basepath ./output
```


4. To execute count_pdx_overlap.py run the following command:
   ptype can be - FDR/BON

```bash
python -m src.tasks._2_twas.count_pdx_overlap --ptype FDR --group UKB --basepath ./output
```

