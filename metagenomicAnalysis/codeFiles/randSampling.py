# Python script randomly selects five samples from each metadata file and downloads corresponding raw sequences from SRA
import pandas as pd
import subprocess
import os

def main():
    # for each group, randSample is executed
    metaBoth = "input/ADHDsingleRuns.tsv"
    randSample(metaBoth, "ADHDsingle")
    
    metaMale = "input/ADHDmultiRuns.tsv"
    randSample(metaMale, "ADHDmulti")
    
    metaFemale = "input/healthRuns.tsv"
    randSample(metaFemale, "health")


def randSample(metaFile, workingFile):
    # number of trials to be rin
    trialNum = 4
    # for each trials, new folder is created
    for i in range (trialNum):
        path = workingFile + "/trial" + str(i+1)
        os.mkdir(path)

        #fastqFiles stores FASTQ files retrieved with the SRA toolkit 
        pathFASTQ = path + "/fastqFiles"
        os.mkdir(pathFASTQ)
        #output stores a metadata file with metadata for selected samples only
        pathOutput = path + "/output"
        os.mkdir(pathOutput)

        # reads in metadata files as a data frame and takes a random sample of 5 rows  
        metaDF = pd.read_csv(metaFile, sep='\t', comment='#')
        IDSample = metaDF.sample(n=5,)

        # metadata of selected samples is outputed to a new metadata file
        outputPath = path + "/output/sampleMeta.tsv"
        IDSample = IDSample.rename(columns={'Run ID': 'sampleID', 'Project ID': 'projectID'})
        IDSample.to_csv(outputPath, sep='\t', index=False)

        # list of sample IDs, used to make calls to SRA toolkit (API)
        IDList = IDSample['sampleID'].astype(str).values.tolist()
        # for each ID, fastq-dump command is used to retrieve for FASTQ files for each selected sample
        # files are zipped (.gz) to reduce download time and make processing with QIIME easier (expected zipped files by default)
        for sra_id in IDList:
            print ("Generating fastq for: " + sra_id)
            fastq_dump = "fastq-dump --outdir " + pathFASTQ + " --gzip " + sra_id
            print ("The command used was: " + fastq_dump)

            # makes command call to actually retrieve file from SRA
            subprocess.call(fastq_dump, shell = True)

            # file is renamed to match QIIME expected naming conventions
            oldNameStr = pathFASTQ + "/" + sra_id + '.fastq.gz'
            newNameStr = pathFASTQ + "/" + sra_id + '_01_L001_R1_001.fastq.gz'
            os.rename(oldNameStr, newNameStr)

if __name__ == "__main__":
    main()
