#!/bin/bash
#$ -N generate_summary_files
#$ -t 1-23
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/generate_summary_files.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/generate_summary_files.err
#$ -l h_rt=12:00:00
#$ -l mem_free=50G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
chrs="${project_directory}data/metadata/chrs.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$chrs")
script="${project_directory}scripts/AGV_LD_variants/generate_summary_files.py"
AGV_LD_variants_directory="${project_directory}data/AGV_LD_variants/data/"
out_directory="${project_directory}data/AGV_LD_variants/"

# run
python3 "$script" --AGV_LD_variants_directory "$AGV_LD_variants_directory" --chr "$chr" --out_directory "$out_directory"
