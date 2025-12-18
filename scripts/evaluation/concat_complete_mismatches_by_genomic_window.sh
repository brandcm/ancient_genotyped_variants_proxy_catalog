#!/bin/bash
#$ -N concat_complete_mismatches_by_genomic_window
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/concat_complete_mismatches_by_genomic_window.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/concat_complete_mismatches_by_genomic_window.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# assign variable
evaluation_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/evaluation/mismatches_by_genomic_window/"

# run
cat "$evaluation_directory"Loschbour_chr*_0.9_complete_mismatches_by_genomic_window.txt | sort -V > "$evaluation_directory"Loschbour_0.9_complete_mismatches_by_genomic_window.txt
cat "$evaluation_directory"Ust_Ishim_chr*_0.9_complete_mismatches_by_genomic_window.txt | sort -V > "$evaluation_directory"Ust_Ishim_0.9_complete_mismatches_by_genomic_window.txt