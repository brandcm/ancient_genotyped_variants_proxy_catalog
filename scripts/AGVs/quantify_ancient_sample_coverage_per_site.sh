#!/bin/bash
#$ -N quantify_ancient_sample_coverage_per_site
#$ -t 1-23
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/quantify_ancient_sample_coverage_per_site.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/quantify_ancient_sample_coverage_per_site.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/AGVs/quantify_ancient_sample_coverage_per_site.py"
VCF_directory="/wynton/group/capra/data/AADR/"
chrs="${project_directory}data/metadata/chrs.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$chrs")
output_directory="${project_directory}data/AGVs/ancient_sample_coverage_per_site/"

# run
mkdir -p "$output_directory"
python3 "$script" --VCF "${VCF_directory}AADR_${chr}.vcf.gz" --output "${output_directory}${chr}_ancient_sample_coverage_per_site.txt"
