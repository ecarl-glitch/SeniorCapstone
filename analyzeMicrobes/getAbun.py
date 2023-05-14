# get realitive abundance data for the health phenotype in project PRJEB11419
# realitive abundance data for ADHD data is downloaded directly from GMrepo, but
# health realtive abundances are for all projects with health phenotype
import requests
import json
import pandas
from pandas.core.frame import DataFrame

def main():
    # opens file with metadata for health phenotypes in project PRJEB11419
    healthIDs = "filteredHealth.tsv"
    getRelAbun(healthIDs, "Health")

    ADHD_IDs = "filteredADHD.tsv"
    getRelAbun(ADHD_IDs, "ADHD")

def getRelAbun(IDfile, phenotype):
    IDs_DF = pandas.read_csv(IDfile, sep='\t', comment='#')
    # creates empty dataframes to store the realtive abundance data for species/genus
    allSpecies =  DataFrame(columns = ['ncbi_taxon_id', 'taxon_rank_level', 'relative_abundance', 'scientific_name'])
    allGenus = DataFrame(columns = ['loaded_uid', 'ncbi_taxon_id', 'taxon_rank_level', 'relative_abundance', 'scientific_name'])

    # loops through health runs and gets realitive abundances for genes and species for each run
    for index, row in IDs_DF.iterrows():
        print(row['Run ID'])
        #submits a query to the GMrepo API with run ID to retrieve realitive abundances for genes and species
        query = {"run_id":row['Run ID']}
        url = 'https://gmrepo.humangut.info/api/getFullTaxonomicProfileByRunID'
        data = requests.post(url, data=json.dumps(query)).json()
        # concats results onto dataframe containing all genus and all species
        species = DataFrame(data.get("species"))
        allSpecies = pandas.concat([allSpecies, species], ignore_index=True, sort=False)

        genus = DataFrame(data.get("genus"))
        allGenus = pandas.concat([allGenus, genus], ignore_index=True, sort=False)
    #outputs resulting dataframes to tsv files
    fileName = "species/allSpecies" + phenotype + ".tsv"
    allSpecies.to_csv(fileName, sep='\t', index=False)
    fileName = "genus/allGenus" + phenotype + ".tsv"
    allGenus.to_csv(fileName, sep='\t', index=False)

if __name__ == "__main__":
    main()
