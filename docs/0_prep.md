
### Step 0: Preparation
<hr />

#### 0.1. Extra cohort SNPs
We need the  files in the following structure:
```

a. --bgen
```
data/steps_0/inputs_{GROUP_NAME}/bgen_{MODEL_NAME}/
```


## How to run Prep pipeline

```bash
python -m src.tasks._0_prep.extra_cohort_snps --coho UKB --basepath ./output
```

