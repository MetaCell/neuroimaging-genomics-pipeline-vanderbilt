# Setup

### Environment 
Create a new environment with the following command:
```bash
conda create -n vander python=3.9
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




Other requirements and installations:

1. Plink2

Get the latest version of plink2 from the following link: 
[https://www.cog-genomics.org/plink/2.0/](https://www.cog-genomics.org/plink/2.0/)
Install plink2 by following the instructions on the website.


Step 1: Download the ZIP file
wget https://s3.amazonaws.com/plink2-assets/plink2_linux_amd_avx2_20240625.zip

Step 2: Unzip the downloaded file
unzip plink2_linux_amd_avx2_20240625.zip

Step 3: Move plink2 to a directory in your PATH (e.g., /usr/local/bin)
Note: This step may require sudo privileges
sudo mv plink2 /usr/local/bin/

Verify installation by checking plink2 version
plink2 --version

2. R 
Install R. This is useful to run the 4th step of the pipeline.
Also install the following R packages:
Start a R session by typing `R` in the terminal and then install the following packages:
```R
install.packages("WebGestaltR")
```

now run the 2_run_webgestalt.r script in the scripts folder.

Commands for executing single tasks:

python -m src.tasks.grex.convert_to_dosage --group HCP --model JTI --basepath ./output





