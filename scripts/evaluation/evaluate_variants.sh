#!/bin/bash
#$ -N evaluate_variants
#$ -t 1-46
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/evaluate_variants.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/evaluate_variants.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
ind_chrs="${project_directory}data/metadata/array_for_evaluation_VCF_filtering.txt"
ind=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$ind_chrs")
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $2}' "$ind_chrs")
evaluation_directory="${project_directory}data/evaluation/"
script="${project_directory}scripts/evaluation/evaluate_variants.py"
LD_file="${evaluation_directory}${chr}_R2_filtered_EUR_AGV_LD_variants.txt.gz"
evaluation_variants="${evaluation_directory}${ind}_${chr}_hg38.txt.gz"
LD_thresholds=('0.5' '0.6' '0.7' '0.8' '0.9' )

# run
mkdir -p "${evaluation_directory}mismatches"
for LD_threshold in ${LD_thresholds[@]}; do python3 "$script" --LD_file "$LD_file" --evaluation_variants "$evaluation_variants" --LD_threshold "$LD_threshold" --output_mismatch "${evaluation_directory}mismatches/${ind}_${chr}_minimum_R2_${LD_threshold}_mismatches.txt" --output_stats "${evaluation_directory}${ind}_evaluation_statistics.txt"; done