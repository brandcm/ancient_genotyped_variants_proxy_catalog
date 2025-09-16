#!/bin/bash
#$ -N concat_ancient_sample_coverage_per_site
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/concat_ancient_sample_coverage_per_site.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/concat_ancient_sample_coverage_per_site.err
#$ -l h_rt=1:00:00
#$ -l mem_free=10G

# change to temp directory
cd "$TMPDIR"

# assign variable
AGV_sample_coverage_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/ancient_sample_coverage_per_site/"

# run
head -n 1 "${AGV_sample_coverage_directory}chr1_ancient_sample_coverage_per_site.txt" > header.txt
for chr in chr{1..22} chrX; do tail -n +2 "${AGV_sample_coverage_directory}${chr}_ancient_sample_coverage_per_site.txt" >> coverage.txt; done
sort -V coverage.txt > sorted_coverage.txt
cat header.txt sorted_coverage.txt > "${AGV_sample_coverage_directory}ancient_sample_coverage_per_site.txt"
gzip "${AGV_sample_coverage_directory}ancient_sample_coverage_per_site.txt"