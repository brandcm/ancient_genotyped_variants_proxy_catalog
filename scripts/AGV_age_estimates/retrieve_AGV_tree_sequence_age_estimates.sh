#!/bin/bash
#$ -N retrieve_AGV_tree_sequence_age_estimates
#$ -t 1-22
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/retrieve_AGV_tree_sequence_age_estimates.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/retrieve_AGV_tree_sequence_age_estimates.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate tskit

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/AGV_age_estimates/retrieve_tree_sequence_age_estimates.py"
age_estimates_directory="${project_directory}/data/AGV_age_estimates/"
tree_sequences_directory="/wynton/group/capra/data/Wohns_et_al_2022_tree_sequences/"
output_directory="${age_estimates_directory}tree_sequence_age_estimates/"

# run
mkdir -p "$output_directory"
python3 "$script" --variants "${project_directory}data/AGVs/AGVs_hg38.bed" --chr "chr${SGE_TASK_ID}" --tree_sequences_directory "$tree_sequences_directory" --output "${output_directory}AGVs_chr${SGE_TASK_ID}.txt"