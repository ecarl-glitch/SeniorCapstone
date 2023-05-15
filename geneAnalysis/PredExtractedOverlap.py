import requests
import json
import pandas as pd

KEGGmetabolites = "output/metaboliteKEGG.tsv"
KEGGmetabolitesDF = pd.read_csv(KEGGmetabolites, sep='\t', comment='#')
KEGGmetaboliteList = KEGGmetabolitesDF['MetaboliteName'].tolist()

trpNetMetabolite = "trpNet/TrpNetMicrobeFromMetabolite.csv"
trpNetMetaboliteDF = pd.read_csv(trpNetMetabolite, comment='#')
trpNetMetaboliteList = trpNetMetaboliteDF['Metabolite'].tolist()

# prints list of shared metabolites
metaboliteOverlap = list((set(KEGGmetaboliteList)&set(trpNetMetaboliteList)))

for i in metaboliteOverlap:
    print(i)


passedMicrobes = "input/genusPassed(0.05).tsv"
passedMicrobesDF = pd.read_csv(passedMicrobes, sep='\t', comment='#')
passedMicrobesList = passedMicrobesDF['scientific_name'].tolist()


trpNetMicrobe = "trpNet/TrpNetMetaboliteFromMicrobes.csv"
trpNetMicrobeDF = pd.read_csv(trpNetMicrobe, comment='#')
trpNetMicrobeList = trpNetMicrobeDF['Taxa'].tolist()

# prints list of shared microbes
microbeOverlap = list((set(passedMicrobesList)&set(trpNetMicrobeList)))

for i in microbeOverlap:
    print(i)
