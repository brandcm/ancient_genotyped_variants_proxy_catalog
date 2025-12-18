#!/bin/bash
#$ -N identify_selection_GWAS_largest_effect_loci_proxies
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/identify_selection_GWAS_largest_effect_loci_proxies.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/identify_selection_GWAS_largest_effect_loci_proxies.err
#$ -l h_rt=2:00:00
#$ -l mem_free=5G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/selection_GWAS_loci_allele_frequency_trajectories/identify_selection_GWAS_largest_effect_loci_proxies.py"
AGV_LD_variant_directory="${project_directory}data/AGV_LD_variants/"
selection_directory="${project_directory}data/selection_GWAS_loci_allele_frequency_trajectories/"

# run
python3 "$script" --effect_loci_file "${selection_directory}Akbari_et_al_2024_selection_BMI_GWAS_largest_effect_loci.txt" \
--AGV_LD_variant_directory "$AGV_LD_variant_directory" \
--output "${selection_directory}Akbari_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxies.txt"

python3 "$script" --effect_loci_file "${selection_directory}Akbari_et_al_2024_selection_height_GWAS_largest_effect_loci.txt" \
--AGV_LD_variant_directory "$AGV_LD_variant_directory" \
--output "${selection_directory}Akbari_et_al_2024_selection_height_GWAS_largest_effect_loci_proxies.txt"

python3 "$script" --effect_loci_file "${selection_directory}Irving_Pease_et_al_2024_selection_BMI_GWAS_largest_effect_loci.txt" \
--AGV_LD_variant_directory "$AGV_LD_variant_directory" \
--output "${selection_directory}Irving_Pease_et_al_2024_selection_BMI_GWAS_largest_effect_loci_proxies.txt"

python3 "$script" --effect_loci_file "${selection_directory}Irving_Pease_et_al_2024_selection_height_GWAS_largest_effect_loci.txt" \
--AGV_LD_variant_directory "$AGV_LD_variant_directory" \
--output "${selection_directory}Irving_Pease_et_al_2024_selection_height_GWAS_largest_effect_loci_proxies.txt"