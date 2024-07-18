# Setup

### Environment 
Create a new environment with the following command:
```bash
conda create -n vander python=3.9.11
```

Activate the environment:
```bash
conda activate vander
```

### Install dependencies
Install the dependencies with the following command:
```bash
pip install -r requirements.txt
```

Softwares used:
- Python 3.9.11
- MetaXcan 
- regenie 


Other requirements and installations:
- Plink2, bgenix, and R. 
TO read more about the installation guide - follow - [Installation guide](docs/installation_guide.md) 



DATA requirements - 
[1st step - GREX](docs/1_grex.md)
[2nd step - TWAS](docs/2_twas.md)
[3rd step - GWAS](docs/3_gwas.md)
[4th step - WEBG](docs/4_webg.md)
[5th step - POLY](docs/5_poly.md)



# Running the pipeline

#### Configure the project base path for your machine in the [config.py](src/config/Config.py) file's `PROJECT_BASE_PATH` variable.

TO run the entire workflow:
```bash
python -m src.workflow
```




To execute a single tasks: (example for GREX - convert to dosage)
```bash
python -m src.tasks._1_grex.convert_to_dosage --group HCP --model JTI --basepath ./output
```



