#!/bin/bash

# change directories
cd /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/TopLD/data

# define variables
ancestry_groups=('AFR' 'EAS' 'EUR' 'SAS' )
chrs=('chr1' 'chr2' 'chr3' 'chr4' 'chr5' 'chr6' 'chr7' 'chr8' 'chr9' 'chr10' 'chr11' 'chr12' 'chr13' 'chr14' 'chr15' 'chr16' 'chr17' 'chr18' 'chr19' 'chr20' 'chr21' 'chr22' 'chrX' )

# run
for ancestry_group in ${ancestry_groups[@]}; do for chr in ${chrs[@]}; do wget "http://topld.genetics.unc.edu/downloads/downloads/${ancestry_group}/SNV/${ancestry_group}_${chr}_no_filter_0.2_1000000_LD.csv.gz" && echo "$ancestry_group $chr LD file download complete"; done; done
for ancestry_group in ${ancestry_groups[@]}; do for chr in ${chrs[@]}; do wget "http://topld.genetics.unc.edu/downloads/downloads/${ancestry_group}/SNV/${ancestry_group}_${chr}_no_filter_0.2_1000000_info_annotation.csv.gz" && echo "$ancestry_group $chr annotation file download complete"; done; done
