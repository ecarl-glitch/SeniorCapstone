# Input Files
Metagenome information obtained from [GMRepo](https://gmrepo.humangut.info/home) on 02/20/2023 <br/> 

<b>```healthRuns.tsv```</b> contains metadata for samples with Health phenotype (Manually filtered to PRJEB11419 samples only) <br/> 
<i>GMrepo Query: </i> 
``` 
disease = 'D006262' AND ( host_age BETWEEN 20 AND 69 AND BMI BETWEEN 18.5 AND 30 AND nr_diseases <= 1 AND QCStatus = 1 AND experiment_type = 'Amplicon' AND nr_reads_sequenced >= 1250 )
```

<b>```ADHDsingleRuns.tsv```</b> contains metadata for samples with ADHD phenotype only <br/>
<i>GMrepo Query: </i>
``` 
disease = 'D001289' AND ( host_age BETWEEN 20 AND 69 AND BMI BETWEEN 18.5 AND 30 AND nr_diseases <= 1 AND QCStatus = 1 AND experiment_type = 'Amplicon' AND nr_reads_sequenced >= 1250 ) 
```

<b>```ADHDmultiRuns.tsv```</b> contains metadata for samples with ADHD phenotype and at least one other phenotype <br/>
<i>GMrepo Query: </i>
``` 
disease = 'D001289' AND ( host_age BETWEEN 20 AND 69 AND BMI BETWEEN 18.5 AND 30 AND nr_diseases > 1 AND QCStatus = 1 AND experiment_type = 'Amplicon' AND nr_reads_sequenced >= 1250 ) 
```
<br/>

# Code

Overview of Procedure 
1. Execute <b>```randSampling.py```</b>
2. Execute <b>```runTrials.sh```</b> - calls qiime1.sh on each trial
3. Review table.qzv of each trial to determine appropriate sampling depth and maximum sampling depth
4. Modify these variables in qiime2.sh (samplingDepth, maxDepth)
5. Execute modified <b>```runTrials.sh```</b> - calls qiime2.sh on each trial
   * see file comments for modification instructions
 

<b>```qiime1.sh```</b> and <b>```qiime2.sh```</b> use modified QIIME commands from https://docs.qiime2.org/2023.2/tutorials/moving-pictures-usage/
* [QIIME 2](https://qiime2.org/) used for analysis of human microbiome samples

Prior to running <b>```randSampling.py```</b> and <b>```runTrials.sh```</b>, QIIME 2 and SRA toolkit must be installed and configured. <br/>

For this analysis, conda was used to install the default QIIME 2 environment (qiime2-2022.11)

Installation and configuration instructions for the SRA toolkit can be found [here](https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit) </br>
For this analysis, the <b>Ubuntu Linux 64 bit architecture </b> compiled binary was used. 

Before running <b>```randSampling.py```</b> for the first time, path to SRA toolkit binaries should be appended to ```PATH``` environment variable:
```
export PATH=$PATH:$PWD/sratoolkit.3.0.0-mac64/bin
```
# Results
QIIME 2 output for each indivdual group is avaliable at https://drive.google.com/file/d/15mMvKBp35ONuW3I5Ba-_gSo7R5sVjIfH/view?usp=sharing </br> </br>
QIIME 2 output for all groups together is avaliable at https://drive.google.com/file/d/1TfIiLGR-4r0qDAWqMKof_hNztpAKpoSS/view?usp=sharing
</br></br>
Zipped files uploaded to Google Drive due to GitHub issues
