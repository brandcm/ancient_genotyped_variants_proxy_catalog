#!/bin/bash
#$ -N generate_allele_frequency_matched_random_sample_for_AGV_age_estimates
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/generate_allele_frequency_matched_random_sample_for_AGV_age_estimates.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/generate_allele_frequency_matched_random_sample_for_AGV_age_estimates.err
#$ -l h_rt=1:00:00
#$ -l mem_free=20G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variable
script="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/generate_allele_frequency_matched_random_sample_for_AGV_age_estimates.py"

# run
python3 "$script"