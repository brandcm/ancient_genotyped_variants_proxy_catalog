#!/bin/bash
#$ -N retrieve_selection_GWAS_largest_effect_loci_proxy_AFs
#$ -t 1-22
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/retrieve_selection_GWAS_largest_effect_loci_proxy_AFs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/retrieve_selection_GWAS_largest_effect_loci_proxy_AFs.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/selection_GWAS_loci_allele_frequency_trajectories/retrieve_selection_GWAS_largest_effect_loci_proxy_AFs.py"
selection_directory="${project_directory}data/selection_GWAS_loci_allele_frequency_trajectories/"
VCF_directory="/wynton/group/capra/data/AADR/"

# run
mkdir -p "${selection_directory}proxy_AFs/"

python3 "$script" --rsIDs_file "${selection_directory}Akbari_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxies.txt" \
--chr "chr${SGE_TASK_ID}" \
--VCF "${VCF_directory}AADR_chr${SGE_TASK_ID}.vcf.gz" \
--output "${selection_directory}proxy_AFs/Akbari_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxy_chr${SGE_TASK_ID}_AFs.txt"

python3 "$script" --rsIDs_file "${selection_directory}Akbari_et_al_2024_selection_height_GWAS_largest_effect_loci_proxies.txt" \
--chr "chr${SGE_TASK_ID}" \
--VCF "${VCF_directory}AADR_chr${SGE_TASK_ID}.vcf.gz" \
--output "${selection_directory}proxy_AFs/Akbari_et_al_2024_selection_height_GWAS_largest_effect_loci_proxy_chr${SGE_TASK_ID}_AFs.txt"

python3 "$script" --rsIDs_file "${selection_directory}Irving_Pease_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxies.txt" \
--chr "chr${SGE_TASK_ID}" \
--VCF "${VCF_directory}AADR_chr${SGE_TASK_ID}.vcf.gz" \
--output "${selection_directory}proxy_AFs/Irving_Pease_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxy_chr${SGE_TASK_ID}_AFs.txt"

python3 "$script" --rsIDs_file "${selection_directory}Irving_Pease_et_al_2024_selection_height_GWAS_largest_effect_loci_proxies.txt" \
--chr "chr${SGE_TASK_ID}" \
--VCF "${VCF_directory}AADR_chr${SGE_TASK_ID}.vcf.gz" \
--output "${selection_directory}proxy_AFs/Irving_Pease_et_al_2024_selection_height_GWAS_largest_effect_loci_proxy_chr${SGE_TASK_ID}_AFs.txt"