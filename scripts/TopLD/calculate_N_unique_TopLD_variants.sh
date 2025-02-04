#!/bin/bash
#$ -N calculate_N_unique_TopLD_variants
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/TopLD/calculate_N_unique_TopLD_variants.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/TopLD/calculate_N_unique_TopLD_variants.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variable
script="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/TopLD/calculate_N_unique_TopLD_variants.py"

# run
python3 "$script"