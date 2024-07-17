
### Step 0: Preparation
<hr />

#### 0.1. Extra cohort SNPs
`INPUT`

We need the  files in the following structure:

a. --bgen
```
data/step_0/inputs_{GROUP_NAME}/bgen_{MODEL_NAME}/*
```

`OUTPUT`
output will be vcf files in :
```
output/step_0/inputs_{GROUP_NAME}/vcf_{MODEL_NAME}/*
```



## How to run Prep pipeline

```bash
python -m src.tasks._0_prep.extra_cohort_snps --coho UKB --basepath ./output
```

