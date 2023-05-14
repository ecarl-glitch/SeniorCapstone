#!/bin/sh

#imports sequences to qiime2 - single lane files
qiime tools import --type 'SampleData[SequencesWithQuality]' \
      --input-path fastqFiles \
      --input-format CasavaOneEightSingleLanePerSampleDirFmt \
      --output-path  qiimeOutput/demux-single-end.qza &&

#Deblur used for sequence trimming and quality control
qiime quality-filter q-score \
  --i-demux qiimeOutput/demux-single-end.qza \
  --o-filtered-sequences qiimeOutput/demux-filtered.qza \
  --o-filter-stats qiimeOutput/demux-filter-stats.qza &&

qiime deblur denoise-16S \
  --i-demultiplexed-seqs qiimeOutput/demux-filtered.qza \
  --p-trim-length 125 \
  --p-sample-stats \
  --o-representative-sequences qiimeOutput/rep-seqs-deblur.qza \
  --o-table qiimeOutput/table-deblur.qza \
  --o-stats qiimeOutput/deblur-stats.qza &&

# generates QIIME2 artifacts that summarize statistics from demux/deblur
qiime metadata tabulate \
  --m-input-file qiimeOutput/demux-filter-stats.qza \
  --o-visualization qiimeOutput/demux-filter-stats.qzv &&

qiime deblur visualize-stats \
  --i-deblur-stats qiimeOutput/deblur-stats.qza \
  --o-visualization qiimeOutput/deblur-stats.qzv &&

# creates FeatureTable summary visualization which is used to determine sampling depth and max sampling depth
# max sampling depth is close to median frequence, sampling depth is highest depth possible that maximizes sequences retained
qiime feature-table summarize \
  --i-table qiimeOutput/table-deblur.qza \
  --m-sample-metadata-file output/metaDataAllSamples.tsv \
  --o-visualization qiimeOutput/table.qzv
