# Procedure Overview

1. <b>```geneAnalysis-Cytoscape/hsa00380.xml```</b> was downloaded from KEGG - human tryptophan metabolism pathway
  * used to create <b>```geneAnalysis-Cytoscape/KEGGpathway.cys```</b>
2. <b>```input/KEGGgenes.tsv```</b> was downloaded from KEGG: genes involved in the human tryptophan metabolism pathway
3. <b>```input/disGenADHDquery.tsv```</b> was downloaded from DisGeNet query
 <br>Phenotypes used in query:
    * Child attention deficit disorder, C0004269
    * Cognition Disorders, C0009241  
    * Attention Deficit Disorder, C0041671  
    * Attention Deficit and Disruptive Behavior Disorders, C0236964  
    * Attention-Deficit/Hyperactivity Disorder, Predominantly Inattentive Type, C0339002 
    * Adult attention deficit hyperactivity disorder, C0865424  
    * Attention deficit hyperactivity disorder, C1263846  
    * ATTENTION DEFICIT-HYPERACTIVITY DISORDER, SUSCEPTIBILITY TO, 7, C2751802  
    * Attention deficit hyperactivity disorder, combined type, C2945552  
    * Undifferentiated attention deficit disorder, C3665679  
    * Attention Deficit Hyper Activity, C3844818
4.  <b>```analysisKEGG.py```</b> is executed to find overlap between KEGG genes and DisGeNet genes </br>
  Creates:
  * output/KEGG_ADHD_genes.tsv
  * metaboliteKEGG.csv
5. TrpNet is used to get microbe predictions using  <b>```metaboliteKEGG.csv```</b> metabolites: TrpNetMicrobesFromMetabolites.csv, and metabolite predictions using  <b>```genusPassed(0.05).tsv```</b> (see analyzeMicrobes)
6. <b>```PredExtractedOverlap.py```</b> finds overlap between predictions and extracted microbes/metabolites
