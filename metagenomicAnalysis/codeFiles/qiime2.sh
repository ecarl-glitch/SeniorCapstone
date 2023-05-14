#!/bin/sh
# QIIME commands modified from Moving Pictures Tutorial: https://docs.qiime2.org/2023.2/tutorials/moving-pictures/

# following variables should be modified for each trial
samplingDepth=
maxDepth=

# renames two files for readability
mv qiimeOutput/rep-seqs-deblur.qza qiimeOutput/rep-seqs.qza &&
mv qiimeOutput/table-deblur.qza qiimeOutput/table.qza &&

# summarizes FeatureTable and FeatureData results
qiime feature-table summarize \
  --i-table  qiimeOutput/table.qza \
  --o-visualization  qiimeOutput/table.qzv \
  --m-sample-metadata-file output/sampleMeta.tsv &&

qiime feature-table tabulate-seqs \
  --i-data  qiimeOutput/rep-seqs.qza \
  --o-visualization  qiimeOutput/rep-seqs.qzv &&

# uses mafft to perform multiple sequence alignment of the sequences
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences qiimeOutput/rep-seqs.qza \
  --o-alignment qiimeOutput/aligned-rep-seqs.qza \
  --o-masked-alignment qiimeOutput/masked-aligned-rep-seqs.qza \
  --o-tree qiimeOutput/unrooted-tree.qza \
  --o-rooted-tree qiimeOutput/rooted-tree.qza

# rarefies the FeatureTable to specified depth, computes several alpha and beta measures
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny qiimeOutput/rooted-tree.qza \
  --i-table qiimeOutput/table.qza \
  --p-sampling-depth $samplingDepth \
  --m-metadata-file output/sampleMeta.tsv \
  --output-dir qiimeOutput/core-metrics-results &&

# tests for associations between categorical metadata and alpha diversity metrics
qiime diversity alpha-group-significance \
  --i-alpha-diversity qiimeOutput/core-metrics-results/faith_pd_vector.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --o-visualization qiimeOutput/core-metrics-results/faith-pd-group-significance.qzv &&

qiime diversity alpha-group-significance \
  --i-alpha-diversity qiimeOutput/core-metrics-results/evenness_vector.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --o-visualization qiimeOutput/core-metrics-results/evenness-group-significance.qzv &&

# tests for associations between selected category and perform pairwise testing on beta metrics
qiime diversity beta-group-significance \
  --i-distance-matrix qiimeOutput/core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --m-metadata-column Sex \
  --o-visualization qiimeOutput/core-metrics-results/unweighted-unifrac-Sex-significance.qzv \
  --p-pairwise &&

qiime diversity beta-group-significance \
  --i-distance-matrix qiimeOutput/core-metrics-results/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --m-metadata-column diseaseName \
  --o-visualization qiimeOutput/core-metrics-results/unweighted-unifrac-Sex-significance.qzv \
  --p-pairwise &&

# creates a alpha-rarefaction plot, a visualization alpha diversity as a function of sampling depth
qiime diversity alpha-rarefaction \
  --i-table  qiimeOutput/table.qza \
  --i-phylogeny  qiimeOutput/rooted-tree.qza \
  --p-max-depth $maxDepth \
  --m-metadata-file output/sampleMeta.tsv \
  --o-visualization qiimeOutput/alpha-rarefaction.qzv &&

# taxonomic classifier used for analysis
wget \
  -O "gg-13-8-99-515-806-nb-classifier.qza" \
  "https://data.qiime2.org/2023.2/common/gg-13-8-99-515-806-nb-classifier.qza" &&

#  uses classifier to explore taxonomic composition of the samples
qiime feature-classifier classify-sklearn \
  --i-classifier  gg-13-8-99-515-806-nb-classifier.qza \
  --i-reads  qiimeOutput/rep-seqs.qza \
  --o-classification  qiimeOutput/taxonomy.qza &&

qiime metadata tabulate \
  --m-input-file  qiimeOutput/taxonomy.qza \
  --o-visualization  qiimeOutput/taxonomy.qzv &&
# creates a visualization of taxonomy distributions for samples
qiime taxa barplot \
  --i-table  qiimeOutput/table.qza \
  --i-taxonomy qiimeOutput/taxonomy.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --o-visualization  qiimeOutput/taxa-bar-plots.qzv &&

# clustering with gneiss is used to create heatmaps, both clustering methods are shown
# but only correlation clustering is used
qiime gneiss correlation-clustering \
  --i-table qiimeOutput/table.qza \
  --o-clustering qiimeOutput/hierarchy.qza

qiime gneiss gradient-clustering \
  --i-table qiimeOutput/table.qza \
  --m-gradient-file output/sampleMeta.tsv \
  --m-gradient-column numPhenotypes \
  --o-clustering qiimeOutput/gradient-hierarchy.qza &&

# heat map visualization, this one is by sex, but can use other categorical information
qiime gneiss dendrogram-heatmap \
  --i-table qiimeOutput/table.qza \
  --i-tree qiimeOutput/hierarchy.qza \
  --m-metadata-file output/sampleMeta.tsv  \
  --m-metadata-column Sex \
  --p-color-map seismic \
  --o-visualization qiimeOutput/heatmap-Sex.qzv &&

# produces a FeatureTable artifact for ancom analysis
qiime composition add-pseudocount \
  --i-table qiimeOutput/table.qza \
  --o-composition-table qiimeOutput/comp-table.qza &&

# runs ANCOM by sex
qiime composition ancom \
  --i-table  qiimeOutput/comp-table.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --m-metadata-column Sex \
  --o-visualization  qiimeOutput/ancom-sex.qzv &&

# runs ANCOM by phenotype
qiime composition ancom \
  --i-table  qiimeOutput/comp-table.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --m-metadata-column Sex \
  --o-visualization  qiimeOutput/ancom-diseaseName.qzv &&

# differential abundance testing at taxonomic level 6
qiime taxa collapse \
  --i-table  qiimeOutput/table.qza \
  --i-taxonomy  qiimeOutput/taxonomy.qza \
  --p-level 6 \
  --o-collapsed-table qiimeOutput/table-l6.qza &&

qiime composition add-pseudocount \
  --i-table  qiimeOutput/table-l6.qza \
  --o-composition-table  qiimeOutput/comp-table-l6.qza &&

qiime composition ancom \
  --i-table  qiimeOutput/comp-table-l6.qza \
  --m-metadata-file output/sampleMeta.tsv \
  --m-metadata-column Sex \
  --o-visualization  qiimeOutput/l6-ancom-subject.qzv
