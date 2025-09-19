#!/bin/bash
#$ -N generate_mismatch_BED_file
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/generate_mismatch_BED_file.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/generate_mismatch_BED_file.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/evaluation/generate_mismatch_BED_file.py"
mismatch_output_directory="${project_directory}data/evaluation/mismatches/"

# run
python3 "$script" --mismatch_output_directory "$mismatch_output_directory" --output "${project_directory}data/supplemental_dfs/LD_variant_prediction_mismatches.bed"