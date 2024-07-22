# Replication

#### Run the sample_UKB 

```bash
python -m src.tasks.replication.save_subsample_UKB --basepath ./output --nshuffles 100
```


#### Run the sample_HCP

```bash
python -m src.tasks.replication.save_subsample_HCP --basepath ./output --nshuffles 100
```




#### Run the sample_UKB_HCP_nonTwin
```bash
python -m src.tasks.replication.save_subsample_UKB_HCP_allEuro --basepath ./output --nshuffles 100
```


#### Run the sample_UKB_HCP_allEuro
NOTE this has an input dependencies from the sample_HCP script. So run it after that. 

NOTE: this doesn't work for now. Since there are concatenation errors.  

```bash
python -m src.tasks.replication.save_subsample_UKB_HCP_nonTwin --basepath ./output --nshuffles 100
```


# Run Subsamples 

```bash
python -m src.tasks.replication.run_subsample_assoc --basepath ./output
```