import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import ttest_ind_from_stats

def main():
    genusHealth = "genus/genusassociatedHealth.tsv"
    genusADHD = "genus/genusassociatedADHD.tsv"
    subsetMicrobes(genusHealth, genusADHD, "genus")
    
    speciesHealth = "species/speciesassociatedHealth.tsv"
    speciesADHD = "species/speciesassociatedADHD.tsv"
    subsetMicrobes(speciesHealth, speciesADHD, "species")

def subsetMicrobes(healthFile, diseaseFile, taxonLevel):
    # loads input files into pandas dataframes
    healthDF = pd.read_csv(healthFile, sep='\t', comment='#')
    diseaseDF = pd.read_csv(diseaseFile, sep='\t', comment='#')

    # gets unique NCBI taxon IDs in both dataframes as lists
    diseaseList = pd.unique((diseaseDF['ncbi_taxon_id'])).tolist()
    healthList = pd.unique((healthDF['ncbi_taxon_id'])).tolist()

    # uses the above list to create a dataframe of values shared between the list
    sharedMicrobeList = set(diseaseList) & set(healthList)
    sharedMicrobeDF = diseaseDF.loc[diseaseDF['ncbi_taxon_id'].isin(sharedMicrobeList)]

    # adds the relative abundance values for health phenotype
    sharedMicrobeDF = pd.merge(sharedMicrobeDF, healthDF[['ncbi_taxon_id', 'numRunsWhereFound',
                                                          'meanRelAdun', 'medianRelAdun', 'SDRelAdun']],
                               on=['ncbi_taxon_id'], how='inner', suffixes=(' Disease', ' Health'))

    runTTest(sharedMicrobeDF, taxonLevel)

def runTTest(sharedMicrobeDF, taxonLevel):
    # values obtained manually from GMrepo, number of total valid runs for a phenotype
    sampleNumDisease = 188
    sampleNumHealth = 1390

    sharedMicrobeDF['result'] = ''
    sharedMicrobeDF['tStat'] = ''
    sharedMicrobeDF['pValue'] = ''

    colNames = list(sharedMicrobeDF.columns.values)
    #Pass 0.05
    passedMicrobes5 = pd.DataFrame(columns = colNames)
    #Pass 0.01
    passedMicrobes1 = pd.DataFrame(columns = colNames)
    # for each microbe, runs t-test of relative abundance metrics, and adds to file based on results
    for index,row in sharedMicrobeDF.iterrows():
        meanRelAbuDisease = row['meanRelAdun Disease']
        meanRelAbuHealth = row['meanRelAdun Health']

        sdRelAbuDisease = row['SDRelAdun Disease']
        sdRelAbuHealth = row['SDRelAdun Health']

        tTestResults = ttest_ind_from_stats(mean1=meanRelAbuDisease, std1=sdRelAbuDisease, nobs1=sampleNumDisease,
                             mean2=meanRelAbuHealth, std2=sdRelAbuHealth, nobs2=sampleNumHealth,
                             equal_var = False)
        
        sharedMicrobeDF.at[index, 'tStat'] = tTestResults[0] 
        sharedMicrobeDF.at[index, 'pStat'] = tTestResults[1] 

        if tTestResults[1] <= 0.05:
            sharedMicrobeDF.at[index, 'result'] = "PASS"
            passedMicrobes5 = pd.concat([passedMicrobes5,sharedMicrobeDF.iloc[[index]]])

            if tTestResults[1] <= 0.01:
                passedMicrobes1 = pd.concat([passedMicrobes1,sharedMicrobeDF.iloc[[index]]])
                
        else:
            sharedMicrobeDF.at[index, 'result'] = "FAIL"

    fileName = taxonLevel + "/output/" + taxonLevel + "Results.tsv"
    sharedMicrobeDF.to_csv(fileName, sep='\t')

    fileName = taxonLevel + "/output/" + taxonLevel + "Passed(0.05).tsv"
    passedMicrobes5.to_csv(fileName, sep='\t')
    getCoOccurances(passedMicrobes5, taxonLevel)

    fileName = taxonLevel + "/output/" + taxonLevel + "Passed(0.01).tsv"
    passedMicrobes1.to_csv(fileName, sep='\t')
    getCoOccurances(passedMicrobes1, taxonLevel)

def getCoOccurances(passedMicrobes, taxonLevel):
    # coOccurance files are downloaded from GM repo for the Health and ADHD phenotype
    coOccurDisease = taxonLevel + "/input/" + taxonLevel + "CooccurrenceADHD.tsv"
    coOccurHealth = taxonLevel + "/input/" + taxonLevel + "CooccurrenceHealth.tsv"
    # subsets coOccurance into microbe species found to be differental abundant - used to construct network in Cytoscape
    coOccurDiseaseDF = pd.read_csv(coOccurDisease, sep='\t', comment='#')
    coOccurHealthDF = pd.read_csv(coOccurHealth, sep='\t', comment='#')

    passedMicrobesList = pd.unique((passedMicrobes['ncbi_taxon_id'])).tolist()

    coOccurDiseaseDFShared = coOccurDiseaseDF.loc[coOccurDiseaseDF['NCBI taxon id 1'].isin(passedMicrobesList)]
    coOccurHealthDFShared = coOccurHealthDF.loc[coOccurHealthDF['NCBI taxon id 1'].isin(passedMicrobesList)]

    coOccurDiseaseDF['Result'] = '' 
    
    for index,row in coOccurDiseaseDF.iterrows():
        if row['NCBI taxon id 1'] in passedMicrobesList:
            coOccurDiseaseDF.at[index, 'Result'] = "PASS"

        else:
            coOccurDiseaseDF.at[index, 'Result'] = "FAIL"

    coOccurHealthDF['Result'] = ''
    # indicates if each microbe species/genus has a p-value less than threshold (PASS) or greater (FAIL)
    for index,row in coOccurHealthDF.iterrows():
        if row['NCBI taxon id 1'] in passedMicrobesList:
            coOccurHealthDF.at[index, 'Result'] = "PASS"
        else:
            coOccurHealthDF.at[index, 'Result'] = "FAIL"

    # sends result to output file
    fileName = taxonLevel + "/output/" + taxonLevel + "FilteredCooccurrenceADHD.tsv"
    coOccurDiseaseDFShared.to_csv(fileName, sep='\t')
    print(coOccurDiseaseDFShared)
    
    fileName = taxonLevel + "/output/" + taxonLevel + "FilteredCooccurrenceHealth.tsv"
    coOccurHealthDFShared.to_csv(fileName, sep='\t')

    fileName = taxonLevel + "/output/" + taxonLevel + "ALLCooccurrenceADHD.tsv"
    coOccurDiseaseDF.to_csv(fileName, sep='\t')

    fileName = taxonLevel + "/output/" + taxonLevel + "ALLCooccurrenceHealth.tsv"
    coOccurHealthDF.to_csv(fileName, sep='\t')


if __name__ == "__main__":
    main()
