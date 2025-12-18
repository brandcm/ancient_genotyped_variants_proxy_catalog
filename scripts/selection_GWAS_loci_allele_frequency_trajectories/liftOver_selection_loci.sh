#!/bin/bash
#$ -N liftOver_selection_loci
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/liftOver_selection_loci.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/selection_GWAS_loci_allele_frequency_trajectories/liftOver_selection_loci.err
#$ -l h_rt=1:00:00
#$ -l mem_free=5G

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
selection_directory="${project_directory}data/selection_GWAS_loci_allele_frequency_trajectories/"
liftOver="/wynton/group/capra/bin/liftOver/liftOver"
hg19_hg38_chain="/wynton/group/capra/bin/liftOver/hg19ToHg38.over.chain.gz"

# run
"$liftOver" "${selection_directory}Akbari_et_al_2024_directional_selection_loci_hg19.bed" \
"$hg19_hg38_chain" \
"${selection_directory}Akbari_et_al_2024_directional_selection_loci_hg38.bed" \
"${selection_directory}Akbari_et_al_2024_directional_selection_loci_hg19.unlifted"

"$liftOver" "${selection_directory}Irving_Pease_et_al_2024_directional_selection_loci_hg19.bed" \
"$hg19_hg38_chain" \
"${selection_directory}Irving_Pease_et_al_2024_directional_selection_loci_hg38.bed" \
"${selection_directory}Irving_Pease_et_al_2024_directional_selection_loci_hg19.unlifted"