
### Step 5: POLY
<hr />

#### 5.1. regress_phen
`INPUT`
--phens (already from the step-3 present)
`data/step_3/inputs_GROUP_NAME/phenotypes/PHEN_TYPE.csv`
--covs (already from the step-3 present)
`data/step_3/inputs_GROUP_NAME/covariates.csv`

`OUTPUT`

```bash
output/step_5/outputs_GROUP_NAME/phenotypes/PHEN_TYPE_regr.csv
```
if PHEN_TYPE=vol_mean then 
```bash
output/step_5/outputs_GROUP_NAME/phenotypes/vol_mean_regr.csv
```

#### 5.2. poly_stats

`INPUT`
--subj_path - (already have it from step 3)- `data/step_3/inputs_GROUP_NAME/cohort.txt`
--fams_path - `data/step_5/inputs_GROUP_NAME/demographics.csv`
--twas_path - (already present from previous steps/scripts) - `output/step_2/outputs_GROUP_NAME/twas_JTI/PHEN_TYPE/REGION_NAME.txt`
--grex_path -  (already present from previous steps/scripts) - `step_1/inputs_GROUP_NAME/grex_JTI/REGION_NAME.hdf5`
--phen_path -  (already present from previous steps/scripts) - `step_5/outputs_GROUP_NAME/phenotypes/PHEN_TYPE_regr.csv`

`OUTPUT`
```bash
output/step_5/outputs_GROUP_NAME/polygenic_models/median_ytrue_ypred.hdf5
output/step_5/outputs_GROUP_NAME/polygenic_models/split_r2s.hdf5
output/step_5/outputs_GROUP_NAME/polygenic_models/split_pvs.hdf5
```



#### 5.3. poly_perm_stats

`INPUT`
--subj_path - (already have it from step 3)- `data/step_3/inputs_GROUP_NAME/cohort.txt`
--fams_path - `data/step_5/inputs_GROUP_NAME/demographics.csv`
--twas_path - (already present from previous steps/scripts) - `output/step_2/outputs_GROUP_NAME/twas_JTI/PHEN_TYPE/REGION_NAME.txt`
--grex_path -  (already present from previous steps/scripts) - `step_1/inputs_GROUP_NAME/grex_JTI/REGION_NAME.hdf5`
--phen_path -  (already present from previous steps/scripts) - `step_5/outputs_GROUP_NAME/phenotypes/PHEN_TYPE_regr.csv`


`OUTPUT`
```bash
output/step_5/outputs_GROUP_NAME/polygenic_models/null_tmp/*
output/step_5/outputs_GROUP_NAME/polygenic_models/nulls.hdf5
```


#### 5.4 twas stats
`INPUT`

--twas_path - (already present from previous steps/scripts) - `output/step_2/outputs_GROUP_NAME/twas_JTI/PHEN_TYPE/REGION_NAME.txt`
--grex_path -  (already present from previous steps/scripts) - `step_1/inputs_GROUP_NAME/grex_JTI/REGION_NAME.hdf5`
--phen_path -  (already present from previous steps/scripts) - `step_5/outputs_GROUP_NAME/phenotypes/PHEN_TYPE_regr.csv`



`OUTPUT`

```bash
output/step_5/outputs_GROUP_NAME/polygenic_models/single_stats.hdf5
```







## How to run POLY pipeline
<hr />

1. To execute regress_phen, run the following command:
```bash
python -m src.tasks._5_poly.regress_phen  --basepath ./output --group UKB
```


2. To execute poly_stats, run the following command:
```bash
python -m src.tasks._5_poly.poly_stats  --basepath ./output --group UKB
```

3. TO execute poly_perm_stats, run the following command:
```bash
python -m src.tasks._5_poly.poly_perm_stats  --basepath ./output --group UKB
```

4. To execute twas_stats, run the following command:
```bash
python -m src.tasks._5_poly.twas_stats  --basepath ./output --group UKB
```

