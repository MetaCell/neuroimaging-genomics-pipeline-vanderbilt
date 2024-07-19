### Step 1: GREX - Data Requirements
<hr />

#### 1.1. Convert to dosage. 
`INPUT` - The input is taken from the output of the 0 step. The vcf files are in the folder in the following structure:
```bash
output/step_0/inputs_{GROUP_NAME}/vcf_{MODEL_NAME}/*
```

for GROUP_NAME=UKB and MODEL_NAME=JTI, it should be in 
```bash
output/step_0/inputs_UKB/vcf_JTI/*
```


`OUTPUT` - this will create output in the `output` folder as:
```bash
output/step_1/inputs_{GROUP_NAME}/dosage_{MODEL_NAME}
```
where `GROUP_NAME` is the group name and `MODEL_NAME` is the model name. If we set `HCP` as the group name and `JTI` as the model name, the input folder should be named as `inputs_HCP/vcf_JTI`. And the output folder will be named as `output/input_HCP/dosage_JTI`.


#### 1.2 Infer Grex
We need the model_by_tissue files in the following structure:

**ensure the files inside the models_by_tissue consist of the following files**

grex_model_names = ["Hippocampus", "Amygdala", "Caudate_basal_ganglia",
				"Nucleus_accumbens_basal_ganglia", "Putamen_basal_ganglia",
				"Cerebellar_Hemisphere", "Anterior_cingulate_cortex_BA24", "Frontal_Cortex_BA9"]


a. `--model_db_path`
```
data/aux_files/models_{MODEL_NAME}/models_by_tissue/{MODEL_NAME}_Brain_{grex_model_names}
```


b. (optional) `--text_genotypes`
this is generated from the previous step - `1.1. Convert to dosage` and can be found in the following structure:
```
output/step_0/input_{GROUP_NAME}/dosage_{MODEL_NAME}
```

so for GROUP_NAME = HCP and MODEL_NAME = JTI, the path should be:
```
output/input_HCP/dosage_JTI
```


c. `--text_sample_ids`
We need the cohort.txt from the following structure:

```
data/input_{GROUP_NAME}/cohort.txt
```

so for GROUP_NAME = HCP, the path should be:
```
data/input_HCP/cohort.txt
```


`OUTPUT`
The following output will be generated as hdf5 files in the `output` folder:

`--prediction_output`

```
output/input_{GROUP_NAME}/grex_{MODEL_NAME}
```
and the logs can be found in  `--prediction_summary_output`
```
output/input_{GROUP_NAME}/grex_{MODEL_NAME}/logs
```


## How to run GREX pipeline

1. To execute convert_to_dosage, run the following command:
```bash
python -m src.tasks._1_grex.convert_to_dosage --group UKB --model JTI --basepath ./output
```

2. To execute infer_grex, run the following command:
```bash
python -m src.tasks._1_grex.infer_grex --group UKB --model JTI --basepath ./output
```
