#!/bin/bash
#$ -N filter_AGV_LD_variants_for_evaluation
#$ -t 1-23
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/filter_AGV_LD_variants_for_evaluation.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/filter_AGV_LD_variants_for_evaluation.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
AGV_LD_variants_directory="${project_directory}data/AGV_LD_variants/data/"
chrs="${project_directory}data/metadata/chrs.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$chrs")
output_directory="${project_directory}data/evaluation/EUR_AGV_LD_variants/"

# run
mkdir -p "$output_directory"
zcat "${AGV_LD_variants_directory}EUR_${chr}_AGV_LD_variants.txt.gz" | awk '($5 >= 0.5) && ($2 ~ /^[0-9]+:[ACGT]:[ACGT]$/) && ($3 ~ /^[0-9]+:[ACGT]:[ACGT]$/) {print $2,$3,$5,$7}' OFS='\t' - > "${output_directory}${chr}_R2_filtered_EUR_AGV_LD_variants.txt"
gzip "${output_directory}${chr}_R2_filtered_EUR_AGV_LD_variants.txt"