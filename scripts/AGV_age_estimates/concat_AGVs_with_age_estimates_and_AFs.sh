#!/bin/bash
#$ -N concat_AGVs_with_age_estimates_and_AFs
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/concat_AGVs_with_age_estimates_and_AFs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/concat_AGVs_with_age_estimates_and_AFs.err
#$ -l h_rt=1:00:00
#$ -l mem_free=10G

# change to temp directory
cd "$TMPDIR"

# assign variable
AGV_age_estimates_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_age_estimates/"

# run
head -n 1 "${AGV_age_estimates_directory}chr1_AGVs_with_age_estimates_and_AFs.txt" > header.txt
for chr in chr{1..22}; do tail -n +2 "${AGV_age_estimates_directory}${chr}_AGVs_with_age_estimates_and_AFs.txt" >> estimates.txt; done
sort -k2n,2 -k3n,3 estimates.txt > sorted_estimates.txt
cat header.txt sorted_estimates.txt > "${AGV_age_estimates_directory}AGVs_with_age_estimates_and_AFs.txt"
gzip "${AGV_age_estimates_directory}AGVs_with_age_estimates_and_AFs.txt"