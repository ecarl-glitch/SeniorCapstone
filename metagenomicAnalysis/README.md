Metagenome information obtained from [GMRepo](https://gmrepo.humangut.info/home) on 02/20/2023 <br/> 

<b>healthRuns.tsv</b> contains metadata for samples with Health phenotype (Manually filtered to PRJEB11419 samples only) <br/> 
GMrepo Query: ``` disease = 'D006262' AND ( host_age BETWEEN 20 AND 69 AND BMI BETWEEN 18.5 AND 30 AND nr_diseases <= 1 AND QCStatus = 1 AND experiment_type = 'Amplicon' AND nr_reads_sequenced >= 1250 ) ```

<b>ADHDsingleRuns.tsv</b> contains metadata for samples with ADHD phenotype only <br/>
GMrepo Query: ``` disease = 'D001289' AND ( host_age BETWEEN 20 AND 69 AND BMI BETWEEN 18.5 AND 30 AND nr_diseases <= 1 AND QCStatus = 1 AND experiment_type = 'Amplicon' AND nr_reads_sequenced >= 1250 ) ```

<b>ADHDmultiRuns.tsv</b> contains metadata for samples with ADHD phenotype and at least one other phenotype <br/>
GMrepo Query: ``` disease = 'D001289' AND ( host_age BETWEEN 20 AND 69 AND BMI BETWEEN 18.5 AND 30 AND nr_diseases > 1 AND QCStatus = 1 AND experiment_type = 'Amplicon' AND nr_reads_sequenced >= 1250 ) ```
