
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
or remove the comment to install WebGestaltR from the script. 
now run the 2_run_webgestalt.r script in the scripts folder.

3. bgenix

Download the precompiled bgenix binary from the following link:
```bash
wget https://www.chg.ox.ac.uk/~gav/resources/bgen_v1.1.4-Ubuntu16.04-x86_64.tgz
```


Extract the downloaded file:
```bash
tar -xvzf bgen_v1.1.4-Ubuntu16.04-x86_64.tgz && rm bgen_v1.1.4-Ubuntu16.04-x86_64.tgz && mv bgen_v1.1.4-Ubuntu16.04-x86_64 bgenix 
```

Move the extracted bgenix folder to software folder:
```bash
mkdir -p software && mv bgenix software/
```

