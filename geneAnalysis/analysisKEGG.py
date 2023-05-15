# This script uses gene-disease associations obtained from online databases
# to determine which genes in KEGG pathway hsa00380 might be associated with ADHD
import pandas as pd
import subprocess
import os

# Data downloaded from disGeNet, from query of ADHD gene-disease associations
# (retrieved April 23rd)
#phenotypes used in query:
    #Child attention deficit disorder, C0004269
    #Cognition Disorders, C0009241  
    #Attention Deficit Disorder, C0041671  
    #Attention Deficit and Disruptive Behavior Disorders, C0236964  
    #Attention-Deficit/Hyperactivity Disorder, Predominantly Inattentive Type, C0339002 
    #Adult attention deficit hyperactivity disorder, C0865424  
    #Attention deficit hyperactivity disorder, C1263846  
    #ATTENTION DEFICIT-HYPERACTIVITY DISORDER, SUSCEPTIBILITY TO, 7, C2751802  
    #Attention deficit hyperactivity disorder, combined type, C2945552  
    #Undifferentiated attention deficit disorder, C3665679  
    #Attention Deficit Hyper Activity, C3844818 
disGenes = "input/disGenADHDquery.tsv"
disGenes_DF = pd.read_csv(disGenes, sep='\t', comment='#')
disGenesList = (disGenes_DF["Gene"].tolist())

# csv file contains pathway data downloaded from KEGG for pathway hsa00380
# 00380 is tryptophan metabolism
# (retrieved April 23rd)
KEGG_Pathway = "input/KEGG_ADHD_genes.tsv"
KEGG_Pathway_DF = pd.read_csv(KEGG_Pathway, sep='\t', comment='#')
print(KEGG_Pathway_DF['KEGG_NODE_TYPE'])
# selects for gene entries in pathway KEGG_Pathway_DF file
KEGG_Pathway_DF_Filtered = KEGG_Pathway_DF[KEGG_Pathway_DF['KEGG_NODE_TYPE'] == 'gene']
print(KEGG_Pathway_DF_Filtered)
# creates a list of gene names of genes in the pathway
KEGG_PathwayList = (KEGG_Pathway_DF_Filtered['KEGG_NODE_LABEL_LIST_FIRST'].tolist())

print(KEGG_PathwayList)

# List of genes in datasets that are in the KEGG pathway hsa00380
sharedDis = set(disGenesList) & set(KEGG_PathwayList)
print(sharedDis)
disGenes_DF = disGenes_DF.loc[disGenes_DF['Gene'].isin(sharedDis)]
# ---

#KEGG_Pathway_DF_Compounds = KEGG_Pathway_DF[KEGG_Pathway_DF['KEGG_NODE_TYPE'] == 'compound'].isin(
KEGG_Pathway_DF_Filtered = KEGG_Pathway_DF_Filtered.loc[KEGG_Pathway_DF_Filtered['KEGG_NODE_LABEL_LIST_FIRST'].isin(sharedDis)]
KEGG_PathwayRxnList = (KEGG_Pathway_DF_Filtered['KEGG_NODE_REACTIONID'].tolist())

print(KEGG_PathwayRxnList)
KEGG_Pathway_DF_Filtered.to_csv("output/KEGG_ADHD_genes.tsv", sep='\t', index=False)




