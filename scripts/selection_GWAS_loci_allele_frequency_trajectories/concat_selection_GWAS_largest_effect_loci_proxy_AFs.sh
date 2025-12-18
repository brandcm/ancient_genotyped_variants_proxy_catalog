#!/bin/bash
#$ -N concat_selection_GWAS_largest_effect_loci_proxy_AFs
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/concat_selection_GWAS_largest_effect_loci_proxy_AFs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/concat_selection_GWAS_largest_effect_loci_proxy_AFs.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# assign variables
selection_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/selection_GWAS_loci_allele_frequency_trajectories/"
proxy_AFs_directory="${selection_directory}proxy_AFs/"

awk 'FNR==1 && NR!=1 { next } { print }' "${proxy_AFs_directory}"Akbari_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxy_chr*_AFs.txt > "${selection_directory}"Akbari_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxy_AFs.txt
awk 'FNR==1 && NR!=1 { next } { print }' "${proxy_AFs_directory}"Akbari_et_al_2024_selection_height_GWAS_largest_effect_loci_proxy_chr*_AFs.txt > "${selection_directory}"Akbari_et_al_2024_selection_height_GWAS_largest_effect_loci_proxy_AFs.txt
awk 'FNR==1 && NR!=1 { next } { print }' "${proxy_AFs_directory}"Irving_Pease_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxy_chr*_AFs.txt > "${selection_directory}"Irving_Pease_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxy_AFs.txt
awk 'FNR==1 && NR!=1 { next } { print }' "${proxy_AFs_directory}"Irving_Pease_et_al_2024_selection_height_GWAS_largest_effect_loci_proxy_chr*_AFs.txt > "${selection_directory}"Irving_Pease_et_al_2024_selection_height_GWAS_largest_effect_loci_proxy_AFs.txt