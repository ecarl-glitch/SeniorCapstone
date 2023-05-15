# Procedure Overview
1. Get runs from GMrepo for phenotypes in project
  * filteredADHD.tsv
  * filteredHealth.tsv
2. Get co-occurance data from GMrepo for phenotypes 
  * genus/input/genusCooccuranceADHD.tsv
  * genus/input/genusCooccuranceHealth.tsv
  * species/input/speciesCooccuranceADHD.tsv
  * species/input/speciesCooccuranceHealth.tsv
3. Run <b>```getAbun.py```</b> to pull relative abundance information </br>
  Creates:
    * genus/output/allGenusADHD.tsv
    * genus/output/allGenusHealth.tsv
    * species/output/allSpeciesADHD.tsv
    * species/output/allSpeciesHealth.tsv
4. Run <b>```findSigMicrobes.py```</b> to determine differential abundant microbes 
  Creates:
    * species/output/speciesALLCooccurrenceADHD.tsv (ADHD co-occurance file with t-test results)
    * species/output/speciesALLCooccurrenceHealth.tsv (Health co-occurance file with t-test results)
    * species/output/speciesALLCooccurrenceHealth.tsv (subset of microbes in Health co-occurance file)
    * species/output/speciesFilteredCooccurrenceADHD.tsv (subset of microbes in ADHD co-occurance file)
    * species/output/speciesFilteredCooccurrenceHealth.tsv (subset of microbes in Health co-occurance file)
    * species/output/speciesPassed(0.01).tsv (species that had p-value >= 0.01 in two sample t-test) 
    * species/output/speciesPassed(0.05).tsv (species that had p-value >= 0.05 in two sample t-test) 
    * species/output/speciesResults.tsv (relative abundance and t-test results for species that had p-value >= 0.05 in two sample t-test) 
    * genus/output/genusALLCooccurrenceADHD.tsv (ADHD co-occurance file with t-test results)
    * genus/output/genusALLCooccurrenceHealth.tsv (Health co-occurance file with t-test results)
    * genus/output/genusALLCooccurrenceHealth.tsv (subset of microbes in Health co-occurance file)
    * genus/output/genusFilteredCooccurrenceADHD.tsv (subset of microbes in ADHD co-occurance file)
    * genus/output/genusFilteredCooccurrenceHealth.tsv (subset of microbes in Health co-occurance file)
    * genus/output/genusPassed(0.01).tsv (genus that had p-value >= 0.01 in two sample t-test) 
    * genus/output/genusPassed(0.05).tsv (genus that had p-value >= 0.05 in two sample t-test)
    * genus/output/genusResults.tsv (relative abundance and t-test results for genus that had p-value >= 0.05 in two sample t-test) 

<b>```getAbun.py```</b> makes calls to the GMrepo API to get relative abundance information
* <b>```filteredADHD.tsv```</b> and <b>```filteredHealth.tsv```</b> are unique runs for the health and ADHD phenotype in project PREJEB11419
* co-occurance data and run metadata must be downloaded before executing scripts
