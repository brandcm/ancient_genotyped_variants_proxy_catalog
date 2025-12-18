#!/bin/bash
#$ -N identify_AGV_LD_variants
#$ -t 1-92
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/identify_AGV_LD_variants.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/identify_AGV_LD_variants.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
ancestry_group_chrs="${project_directory}data/metadata/chrs_by_ancestry_group.txt"
ancestry_group=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$ancestry_group_chrs")
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $2}' "$ancestry_group_chrs")
dictionary="${project_directory}data/AGVs/AGVs_hg38.pkl"
TopLD_directory="${project_directory}data/TopLD/data/"
out_directory="${project_directory}data/AGV_LD_variants/data/"
script="${project_directory}scripts/AGV_LD_variants/identify_AGV_LD_variants.py"

# run
mkdir -p "$out_directory"
python3 "$script" --dictionary "$dictionary" --ancestry_group "$ancestry_group" --chromosome "$chr" --LD_files_directory "$TopLD_directory" --out_directory "$out_directory"
gzip "${out_directory}${ancestry_group}_${chr}_AGV_LD_variants.txt"
