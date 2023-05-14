# script uses allGenusHealth and allSpeciesHealth files generated in getHealthAbun.py
import pandas as pd

def main():
    # calls getMicrobe function on input files
    allGenus = "genus/allGenusHealth.tsv"
    getMicrobes(allGenus, "Health")
    allSpecies = "species/allSpeciesHealth.tsv"
    getMicrobes(allSpecies, "Health")

    allGenus = "genus/allGenusADHD.tsv"
    getMicrobes(allGenus, "ADHD")
    allSpecies = "species/allSpeciesADHD.tsv"
    getMicrobes(allSpecies, "ADHD")

# function runs calculations for each unique microbe in file and output to a new file
def getMicrobes(microbe, phenotype):
    microbeDF = pd.read_csv(microbe, sep='\t', comment='#')
    print(microbeDF['scientific_name'].value_counts())
    # creates a list of unique microbes in dataframe
    allMicrobeList = microbeDF['scientific_name'].unique().tolist()
    # column name list for new dataframe microbeHealth
    col_names =  ['ncbi_taxon_id', 'taxon_rank_level', 'scientific_name', 'numRunsWhereFound', 'meanRelAdun', 'medianRelAdun', 'SDRelAdun']
    microbeHealth  = pd.DataFrame(columns = col_names)

    # loops through each microbe in the list of unique microbes
    for microbe in allMicrobeList:
        # creates a subset of the microbe dataframe for current microbe
        subsetDF = microbeDF[microbeDF['scientific_name'] == microbe]
        # sets ncbi_taxon_id, taxon_rank_level, and numRunsWhereFound for new dataframe
        ncbi_taxon_id = subsetDF['ncbi_taxon_id'].unique()[0]
        taxon_rank_level = subsetDF['taxon_rank_level'].unique()[0]
        numRunsWhereFound = len(subsetDF.index)
        # calculates mean, median, and std for relative_abundance
        meanRelAdun = subsetDF['relative_abundance'].mean()
        medianRelAdun= subsetDF['relative_abundance'].median()
        SDRelAdun= subsetDF['relative_abundance'].std()

        # adds values to temp dataframe and appends the new data to microbeHealth datafram created prior to loop
        rows_to_append = pd.DataFrame([{'ncbi_taxon_id':ncbi_taxon_id, 'taxon_rank_level':taxon_rank_level, 'scientific_name':microbe, 'numRunsWhereFound':numRunsWhereFound,
                                        'meanRelAdun':meanRelAdun, 'medianRelAdun':medianRelAdun, 'SDRelAdun':SDRelAdun}])
        
        microbeHealth = pd.concat([microbeHealth, rows_to_append])

    # filters dataframe to rows where microbes are in 2+ runs and median relative abundance is at least 0.01
    microbeHealth = microbeHealth[microbeHealth['numRunsWhereFound'] >= 2]
    microbeHealth = microbeHealth[microbeHealth['medianRelAdun'] >= 0.01]
    #sends filtered dataframe to a new output file
    print(taxon_rank_level + " " + phenotype)
    print(microbeHealth)
    fileName = taxon_rank_level + "/" + taxon_rank_level + "associated" + phenotype + ".tsv"
    microbeHealth.to_csv(fileName,  sep='\t', index=False)

if __name__ == "__main__":
    main()
