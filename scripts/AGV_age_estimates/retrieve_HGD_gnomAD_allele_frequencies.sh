#!/bin/bash
#$ -N retrieve_HGD_gnomAD_allele_frequencies
#$ -t 1-22
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/retrieve_HGD_gnomAD_allele_frequencies.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_age_estimates/retrieve_HGD_gnomAD_allele_frequencies.err
#$ -l h_rt=30:00:00
#$ -l mem_free=50G

# load modules
module load CBI
module load bcftools/1.21

# change to temp directory
cd "$TMPDIR"

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
chr="chr$SGE_TASK_ID"
HGD_directory="/wynton/group/capra/data/human_genome_dating/2024-01-02/"
gnomAD_VCFs_directory="/wynton/group/capra/data/wynton_databases/gnomAD/2.1.1/variants/genomes"
output_directory="${project_directory}/data/AGV_age_estimates/gnomAD_AFs/"

# run
zcat "${HGD_directory}atlas.${chr}.csv.gz" | tail -n +5 | awk -F, -v chr_without_prefix="$SGE_TASK_ID" '{print chr_without_prefix,$3-1,$3}' OFS='\t' - | sort -k2n,2 | uniq > "$chr".tmp
bcftools view -R "$chr".tmp -i 'FILTER="PASS"' -v snps "${gnomAD_VCFs_directory}/gnomad.genomes.r2.1.1.sites.${SGE_TASK_ID}.vcf.bgz" --threads 4 | bcftools query -f'%CHROM\t%POS\t%REF\t%ALT{0}\t%AF\n' > "${chr}_HGD_gnomAD_AFs.txt"
mkdir -p "$output_directory"
mv "${chr}_HGD_gnomAD_AFs.txt" "$output_directory"
