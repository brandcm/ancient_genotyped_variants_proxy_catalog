#!/bin/bash
#$ -N evaluate_complete_mismatches_by_genomic_window
#$ -t 1-46
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/evaluate_complete_mismatches_by_genomic_window.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/evaluate_complete_mismatches_by_genomic_window.err
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
script="${project_directory}scripts/evaluation/evaluate_complete_mismatches_by_genomic_window.py"
LD_file="${evaluation_directory}EUR_AGV_LD_variants/${chr}_R2_filtered_EUR_AGV_LD_variants.txt.gz"
evaluation_variants="${evaluation_directory}ancient_genotypes/${ind}_${chr}_hg38.txt.gz"

# run
mkdir -p "${evaluation_directory}mismatches_by_genomic_window/"
python3 "$script" --LD_file "$LD_file" --evaluation_variants "$evaluation_variants" --LD_threshold 0.9 --window_size 50000 --step_size 25000 --output "${evaluation_directory}mismatches_by_genomic_window/${ind}_${chr}_0.9_complete_mismatches_by_genomic_window.txt"