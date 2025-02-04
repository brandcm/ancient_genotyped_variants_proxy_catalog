#!/bin/bash
#$ -N concat_and_map_AGV_gnomAD_allele_frequencies
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/concat_and_map_AGV_gnomAD_allele_frequencies.out
#$ -e /wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/concat_and_map_AGV_gnomAD_allele_frequencies.err
#$ -l h_rt=1:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# change directories
cd /wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants

# assign variables
project_directory="/wynton/group/capra/projects/AADR_proxy_variants/"
TopLD_annotation_script="${project_directory}scripts/1240K_variants/AGVs_TopLD_presence_summary.py"
merge_script="${project_directory}scripts/1240K_variants/merge_AGV_files.py"

# run
# concat gnomAD AFs
cat gnomAD_allele_frequencies/AGV_chr*_gnomAD_allele_frequencies.txt > AFs.tmp

# concat TopLD annotations
#python3 "$TopLD_annotation_script"
cat TopLD_presence_summaries_updated/AGVs_chr*_TopLD_presence_summary.txt | sort -k1,1 > AGVs_TopLD_presence_summary.tmp

# merge
python3 "$merge_script"

# cleanup
#rm AFs.tmp && rm AGVs_TopLD_presence_summary.tmp