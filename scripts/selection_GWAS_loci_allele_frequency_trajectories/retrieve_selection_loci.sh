#!/bin/bash

# assign variable
selection_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/selection_GWAS_loci_allele_frequency_trajectories/"

# run
# Akbari et al. 2024
zcat "${selection_directory}Akbari_et_al_2024_hg19.txt.gz" | awk 'NR>1 && $0 !~ /^#/ && $0 !~ /^CHROM/ && (($11 >= 5.45) || ($11 <= -5.45)) {print "chr"$1,$2-1,$2}' OFS='\t' - > "${selection_directory}Akbari_et_al_2024_directional_selection_loci_hg19.bed"

# Irving-Pease et al. 2024
zcat "${selection_directory}Irving_Pease_et_al_2024_hg19.txt.gz" | tail -n +3 | awk -F '\t' '($21 < 5e-8) {print "chr"$3,$4-1,$4}' OFS='\t' - | sort -u > "${selection_directory}Irving_Pease_et_al_2024_directional_selection_loci_hg19.bed"