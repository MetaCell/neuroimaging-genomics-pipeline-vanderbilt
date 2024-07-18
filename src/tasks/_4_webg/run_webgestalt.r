#!/usr/bin/env Rscript
# install.packages('WebGestaltR')
# install.packages("WebGestaltR", dependencies=TRUE, verbose=TRUE)
library(WebGestaltR) ## downloaded version: 0.4.6		

gmtPath <- args[1]
desPath <- args[2]
jtiPath <- args[3]
innPath <- args[4]
outPath <- args[5]
phens <- args[6]
regs <- args[7]


for (reg in regs) {

    interreg <- grepl('interreg', phens)
    if (interreg) {
        refsPath <- paste(jtiPath, 'genes_8regs.txt', sep='')
    } else {
        refsPath <- paste(jtiPath, reg, '.txt', sep='')
    }
    refsList <- readLines(refsPath)

    genePath <- paste(innPath, reg, '.txt', sep='')
    geneList <- readLines(genePath)

    enrichResult <- WebGestaltR(
        enrichMethod='ORA', 
        organism='hsapiens',
        enrichDatabaseFile=gmtPath, 
        enrichDatabaseType='ensembl_gene_id',
        enrichDatabaseDescriptionFile=desPath,
        interestGene=geneList,
        referenceGene=refsList,
        interestGeneType='ensembl_gene_id',
        referenceGeneType='ensembl_gene_id',
        sigMethod='top',
        topThr=6000,
        isOutput=TRUE,
        outputDirectory=outPath, projectName=reg)

}
