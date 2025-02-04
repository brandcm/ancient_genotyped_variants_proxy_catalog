#!/bin/bash
#$ -N AGVs_TopLD_presence_summary
#$ -t 1-23
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/AGVs_TopLD_presence_summary.out
#$ -e /wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/AGVs_TopLD_presence_summary.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variable
project_directory="/wynton/group/capra/projects/AADR_proxy_variants/"
AGVs_BED="${project_directory}data/1240K_variants/1240K_variants_hg38.bed"
chr_IDs="${project_directory}data/metadata/chrs.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$chr_IDs")
TopLD_directory="${project_directory}data/TopLD/data/"
AGV_LD_variants_directory="${project_directory}data/AGV_LD_variants/data/"
output_directory="${project_directory}data/1240K_variants/TopLD_presence_summaries_updated/"
script="/wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/AGVs_TopLD_presence_summary_updated.py"

# run
mkdir -p "$output_directory"
python3 "$script" --AGVs_BED "$AGVs_BED" --chr "$chr" --TopLD_directory "$TopLD_directory" --AGV_LD_variants_directory "$AGV_LD_variants_directory" --output "${output_directory}AGVs_${chr}_TopLD_presence_summary.txt"
