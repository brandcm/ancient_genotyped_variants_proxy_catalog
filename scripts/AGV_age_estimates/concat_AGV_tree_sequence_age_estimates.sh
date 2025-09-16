#!/bin/bash
#$ -N concat_AGV_tree_sequence_age_estimates
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/concat_AGV_tree_sequence_age_estimates.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/concat_AGV_tree_sequence_age_estimates.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# assign variable
age_estimates_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_age_estimates/"

# run
cat "${age_estimates_directory}"tree_sequence_age_estimates/AGVs_chr*.txt | sort -V > "${age_estimates_directory}AGV_tree_sequence_age_estimates.txt"
gzip "${age_estimates_directory}AGV_tree_sequence_age_estimates.txt"
