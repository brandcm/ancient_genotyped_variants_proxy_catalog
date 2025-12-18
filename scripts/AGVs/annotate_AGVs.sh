#!/bin/bash
#$ -N annotate_AGVs
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/annotate_AGVs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/annotate_AGVs.err
#$ -l h_rt=1:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
AGVs_directory="${project_directory}data/AGVs/"
merge_script="${project_directory}scripts/AGVs/annotate_AGVs.py"

# run
cat "$AGVs_directory"gnomAD_AFs/chr*_AGVs_gnomAD_AFs.txt > "${AGVs_directory}AFs.tmp"
cat "$AGVs_directory"TopLD_presence_summaries/chr*_AGVs_TopLD_presence_summary.txt | sort -k1,1 > "${AGVs_directory}AGVs_TopLD_presence_summary.tmp"
python3 "$merge_script"

# cleanup
rm "${AGVs_directory}"{AFs.tmp,AGVs_TopLD_presence_summary.tmp}