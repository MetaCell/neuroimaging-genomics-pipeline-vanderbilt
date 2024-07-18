
### Step 4: WEBG
<hr />

#### 4.1. Save Predixvu GMT

We need the  files in the following structure:

`INPUT`
```bash	
data/step_4/aux_files/predixvu_assocs.csv.gz
data/step_4/aux_files/predixvu_brain_phecodes.csv
```


`OUTPUT`
output can be seen in 
```bash
output/step_4/aux_files/pdx_nom0.001.des
output/step_4/aux_files/pdx_nom0.001.gmt
```

#### 4.2. Save Interest Sets

`INPUT`
these inputs should already be present in step_2 - from following structure
```bash
data/step_2/outputs_GROUP_NAME/twas_JTI/PHENS/*
data/step_2/outputs_GROUP_NAME/twas_JTI/cross_regs/PHENS/*
```

For GROUP_NAME=UKB and PHENS=vol_mean, the following files are needed:

```bash
data/step_2/outputs_UKB/twas_JTI/vol_mean/*
data/step_2/outputs_UKB/twas_JTI/cross_regs/vol_mean/*
```

`OUTPUT`
```bash
step_4/inputs_GROUP_NAME/enrich_sets/*
```


#### 4.3. Run Webgestalt

`INPUT`
Input is coming from the output of the first step. These are gmt and des files. You can see them in the following structure:
```bash
output/step_4/aux_files/*
```

given that ontol is pdx_nom0.001, the following files are needed:

--gmtPath and --desPath are the paths to the gmt and des files, respectively.
```bash
output/step_4/aux_files/pdx_nom0.001.des
output/step_4/aux_files/pdx_nom0.001.gmt
```

--jtiPath -> This is the folder containing JTI files. The files are in the following structure:
```bash
data/step_4/aux_files/models_JTI/gene_by_tissue/*
```

--innPath -> this is the list of enrich_sets, this is the output of the second step (save_interest_sets). Should be in the following structure:
```bash
output/step_4/inputs_GROUP_NAME/enrich_sets/*
```
here if  GROUP_NAME=UKB 
```bash
output/step_4/inputs_UKB/enrich_sets/*
```




`OUTPUT`
```bash
output/step_4/outputs_GROUP_NAME/enrich_ONTOL/PTYPE_PHENS
```
for GROUP_NAME=UKB, ONTOL=pdx_nom0.001, PTYPE=FDR, and PHENS=vol_mean, it will be 
```bash
output/step_4/outputs_UKB/enrich_pdx_nom0.001/FDR_vol_mean/*
```



#### 4.4 Save Enrichment Summary
The input is the output of the previous step. The output is in the following structure:
`INPUT`
```bash
output/step_4/outputs_GROUP_NAME/enrich_ENRICH_NAME/PTYPE_PHENS/enrichment_results/*
```
If GROUP_NAME=UKB, ENRICH_NAME=pdx_nom0.001, PTYPE=FDR, and PHENS=vol_mean, the input should be:
```bash
output/step_4/outputs_UKB/enrich_pdx_nom0.001/FDR_vol_mean/*
```

`OUTPUT`

This will generate a summary.csv file in the following structure:
```bash
output/step_4/outputs_GROUP_NAME/enrich_ENRICH_NAME/PTYPE_PHENS_interreg/enrichment_summary.csv
```








## How to run WEBG pipeline
<hr />

1. To execute save_predixvu_gmt, run the following command:

```bash
python -m src.tasks._4_webg.save_predixvu_gmt  --basepath ./output
```

2. To execute save_interest_sets, run the following command:

```bash
python -m src.tasks._4_webg.save_interest_sets  --basepath ./output --group UKB --phens vol_mean --ptype FDR
```

3. Run Webgestalt R script

```bash
python -m src.tasks._4_webg.run_webgestalt  --basepath ./output --group UKB --phens vol_mean --ptype FDR --ontol pdx_nom0.001
```
if phens used is vol_mean_interreg then it will be stored in `output/step_4/outputs_UKB/enrich_pdx_nom0.001/FDR_vol_mean_interreg/*`

4. Save Enrichment summary

```bash
python -m src.tasks._4_webg.save_enrich_summary  --basepath ./output --group UKB --phens vol_mean --enrich pdx_nom0.001 --ptype FDR
```