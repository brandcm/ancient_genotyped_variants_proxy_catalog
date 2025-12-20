#!/bin/bash
#$ -N retrieve_AGV_gnomAD_allele_frequencies
#$ -t 1-23
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/retrieve_AGV_gnomAD_allele_frequencies.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/retrieve_AGV_gnomAD_allele_frequencies.err
#$ -l h_rt=24:00:00
#$ -l mem_free=50G

# load modules
module load CBI
module load bcftools/1.21

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
chr_IDs="${project_directory}data/metadata/chrs.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$chr_IDs")
bedfile="${project_directory}data/AGVs/AGVs_hg38.bed"
gnomAD_vcfs_directory="/wynton/group/capra/data/wynton_databases/gnomAD/4.1/vcf/genomes/"
output_directory="${project_directory}data/AGVs/gnomAD_AFs/"

# run
mkdir -p "$output_directory"
bcftools view -R "$bedfile" -v snps "${gnomAD_vcfs_directory}gnomad.genomes.v4.1.sites.${chr}.vcf.bgz" | bcftools query -f'%CHROM\t%POS\t%REF\t%ALT{0}\t%FILTER\t%AF\t%AF_afr\t%AF_eas\t%AF_nfe\t%AF_sas\n' > "${output_directory}${chr}_AGVs_gnomAD_AFs.txt"
