#!/bin/bash
#$ -N retrieve_AGV_gnomAD_allele_frequencies
#$ -t 1-23
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/retrieve_AGV_gnomAD_allele_frequencies.out
#$ -e /wynton/group/capra/projects/AADR_proxy_variants/scripts/1240K_variants/retrieve_AGV_gnomAD_allele_frequencies.err
#$ -l h_rt=24:00:00
#$ -l mem_free=50G

# load modules
module load CBI
module load bcftools/1.21

# assign variables
chr_IDs="/wynton/group/capra/projects/AADR_proxy_variants/data/metadata/chrs.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$chr_IDs")
bedfile="/wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants/1240K_variants_hg38.bed"
gnomAD_vcfs_directory="/wynton/group/capra/data/wynton_databases/gnomAD/4.1/vcf/genomes"
output_directory="/wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants/gnomAD_allele_frequencies/"

# run
mkdir -p "$output_directory"
bcftools view -R "$bedfile" -v snps "$gnomAD_vcfs_directory"/gnomad.genomes.v4.1.sites."$chr".vcf.bgz | bcftools query -f'%CHROM\t%POS\t%REF\t%ALT{0}\t%FILTER\t%AF\t%AF_afr\t%AF_eas\t%AF_nfe\t%AF_sas\n' > "${output_directory}AGV_${chr}_gnomAD_allele_frequencies.txt"
