FROM python:3.9-bookworm
# Install updates
RUN apt update
# Install package dependencies
RUN apt install -y r-base-core build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev

RUN which Rscript
# Install r libraries for step 4
RUN Rscript -e "install.packages('WebGestaltR')"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download and install plink2
RUN wget https://s3.amazonaws.com/plink2-assets/plink2_linux_amd_avx2_20240704.zip
RUN mv plink2_linux_amd_avx2_20240704.zip /tmp && cd /tmp && unzip plink2_linux_amd_avx2_20240704.zip && mv plink2 /usr/bin

# Download and install bgenix
RUN wget https://www.chg.ox.ac.uk/~gav/resources/bgen_v1.1.4-Ubuntu16.04-x86_64.tgz
RUN mv bgen_v1.1.4-Ubuntu16.04-x86_64.tgz /tmp && \
    cd /tmp && \
    tar -xzvf bgen_v1.1.4-Ubuntu16.04-x86_64.tgz && \
    mv bgen_v1.1.4-Ubuntu16.04-x86_64/bgenix /usr/bin

COPY . .
ENV BASE_PATH=/usr/src/app
ENV PLINK_PATH=/usr/bin/plink2
ENV BGENIX_PATH=/usr/bin/bgenix
ENTRYPOINT ["/bin/bash"]
