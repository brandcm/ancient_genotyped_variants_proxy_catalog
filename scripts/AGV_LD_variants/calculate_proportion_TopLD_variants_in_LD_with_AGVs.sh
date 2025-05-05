#!/bin/bash
#$ -N calculate_proportion_TopLD_variants_in_LD_with_AGVs
#$ -t 1-4
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/calculate_proportion_TopLD_variants_in_LD_with_AGVs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/calculate_proportion_TopLD_variants_in_LD_with_AGVs.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/AGV_LD_variants/calculate_proportion_TopLD_variants_in_LD_with_AGVs.py"
ancestry_groups=('AFR' 'EAS' 'EUR' 'SAS' )
ancestry_group=${ancestry_groups[$SGE_TASK_ID-1]}
out_directory="${project_directory}data/AGV_LD_variants/"

# run
python3 "$script" --ancestry_group "$ancestry_group" --out "${out_directory}${ancestry_group}_TopLD_variants_in_LD_with_AGVs.txt"