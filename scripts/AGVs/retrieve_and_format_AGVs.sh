#!/bin/bash
#$ -N retrieve_and_format_AGVs
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/retrieve_and_format_AGVs.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGVs/retrieve_and_format_AGVs.err
#$ -l h_rt=1:00:00
#$ -l scratch=5G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate ancestral_allele

# change to temp directory
cd "$TMPDIR"

# assign variables
AGVs="/wynton/group/capra/data/wynton_databases/ancient_dna/V54.1.p1/v54.1.p1_1240K_public.snp"
liftOver_directory="/wynton/group/capra/bin/liftOver/"
liftOver="${liftOver_directory}liftOver"
hg19_hg38_chain="${liftOver_directory}hg19ToHg38.over.chain.gz"
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/AGVs/check_reference_bases_in_AGVs_hg38_BED.py"
hg38_fasta="/wynton/group/capra/data/hg38_fasta/2022-03-14/hg38.fa"
out_directory="${project_directory}data/AGVs/"

# run
awk '{ chr = $2 == "23" ? "X" : ($2 == "24" ? "Y" : $2); print "chr"chr,$4-1,$4,$5,$6,$1}' OFS='\t' "$AGVs" > AGVs_hg19.bed
awk '{print $1,$2,$3,$4":"$5":"$6}' OFS='\t' AGVs_hg19.bed > AGVs_hg19.tmp
"$liftOver" AGVs_hg19.tmp "$hg19_hg38_chain" AGVs_hg38.tmp AGVs_hg19.unlifted
awk -F'[\t:]' '{print $1,$2,$3,$4,$5,$6}' OFS='\t' AGVs_hg38.tmp > AGVs_hg38.tmp2
python3 "$script" --fasta "$hg38_fasta" --bed AGVs_hg38.tmp2 --output AGVs_hg38.bed
mkdir -p "$out_directory"
mv AGVs_hg19.bed "$out_directory" && mv AGVs_hg19.unlifted "$out_directory" && mv AGVs_hg38.bed "$out_directory"
