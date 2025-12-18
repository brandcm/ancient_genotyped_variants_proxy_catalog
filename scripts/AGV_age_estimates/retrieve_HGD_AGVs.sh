#!/bin/bash
#$ -N retrieve_HGD_AGVs
#$ -t 1-22
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/retrieve_HGD_AGVs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/retrieve_HGD_AGVs.err
#$ -l h_rt=1:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# change to temp directory
cd "$TMPDIR"

# assign variables
HGD_directory="/wynton/group/capra/data/human_genome_dating/2024-01-02/"
chr="chr$SGE_TASK_ID"
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
AGV_age_estimates_directory="${project_directory}data/AGV_age_estimates/"
AGVs="${project_directory}data/AGVs/AGVs_hg19.bed"
script="${project_directory}scripts/AGV_age_estimates/map_gnomAD_AFs.py"

# run
zcat "${HGD_directory}atlas.${chr}.csv.gz" | tail -n +5 | sed 's/, /\t/g' > "${chr}.tmp"
awk 'NR==FNR {a[$1, $3, $4, $5]; next} ("chr"$2, $3, $4, $5) in a {print $0}' "$AGVs" "${chr}.tmp" > "${chr}_HGD_AGVs.tmp"
python3 "$script" --HGD_file "${chr}_HGD_AGVs.tmp" --gnomAD_AFs_file "${AGV_age_estimates_directory}gnomAD_AFs/${chr}_HGD_gnomAD_AFs.txt" --output "${AGV_age_estimates_directory}${chr}_AGVs_with_age_estimates_and_AFs.txt"