#!/bin/bash

# Assign variable
output_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/selection_GWAS_loci_allele_frequency_trajectories/"

# run
# BMI
wget https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90179001-GCST90180000/GCST90179150/harmonised/GCST90179150.h.tsv.gz
zcat GCST90179150.h.tsv.gz | awk '($8 < 5e-8) {print "chr"$1,$2-1,$2,$3,$4,$9,$5,$7,$8}' OFS='\t' - > "${output_directory}Koskeridis_et_al_2022_GCST90179150_BMI_significant_loci_hg38_betas_and_AFs.bed"
rm GCST90179150.h.tsv.gz

# Height
wget https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90245001-GCST90246000/GCST90245992/harmonised/GCST90245992.h.tsv.gz
zcat GCST90245992.h.tsv.gz | awk '($8 < 5e-8) {print "chr"$1,$2-1,$2,$3,$4,$9,$5,$7,$8}' OFS='\t' - > "${output_directory}Yengo_et_al_2022_GCST90245992_significant_loci_hg38_betas_and_AFs.bed"
rm GCST90245992.h.tsv.gz