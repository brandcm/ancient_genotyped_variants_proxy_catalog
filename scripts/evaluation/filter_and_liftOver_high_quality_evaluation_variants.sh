#!/bin/bash
#$ -N filter_and_liftOver_high_quality_evaluation_variants
#$ -t 1-46
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/filter_and_liftOver_high_quality_evaluation_variants.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/evaluation/filter_and_liftOver_high_quality_evaluation_variants.err
#$ -l h_rt=8:00:00
#$ -l mem_free=20G

# load modules
module load CBI
module load bcftools/1.21

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate ancestral_allele

# change into temporary directory
cd "$TMPDIR"

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
ind_chrs="${project_directory}data/metadata/array_for_evaluation_VCF_filtering.txt"
ind=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$ind_chrs")
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $2}' "$ind_chrs")
evaluation_directory="${project_directory}data/evaluation/"
hg38_fasta="/wynton/group/capra/data/hg38_fasta/2022-03-14/hg38.fa"

if [[ "$ind" == "Loschbour" ]]; then
	VCF_directory="/wynton/group/capra/data/Loschbour/2024-09-21/"
else
	VCF_directory="/wynton/group/capra/data/Ust_Ishim/2024-09-21/"
fi

liftOver="/wynton/group/capra/bin/liftOver/liftOver"
hg19_hg38_chain="/wynton/group/capra/bin/liftOver/hg19ToHg38.over.chain.gz"

# write filtering function
genotype_filter () {
	bcftools view -R "${VCF_directory}${chr}_mask.bed.gz" "${VCF_directory}${chr}_mq25_mapab100.vcf.gz" | # apply MPI masks
	bcftools filter -S . -i 'FMT/DP>=10 & FMT/GQ>=30' | # set low-quality genotypes to missing
	bcftools view -e 'FMT/GT="./."' -O z -o "$chr".filtered.vcf.gz # exclude missing genotypes then output
}

# run
genotype_filter
bcftools query -f '%CHROM\t%POS\t%REF\t[%ALT]\t[%GT]\n' "$chr".filtered.vcf.gz | awk '{alleles[1] = $3; split($4, alts, ","); for (a in alts) alleles[1 + a] = alts[a]; split($5, gt, "/"); genotype = ""; for (i = 1; i <= length(gt); i++) {genotype = genotype (i > 1 ? "," : "") (gt[i] == "." ? "." : alleles[gt[i] + 1])} print $1, $2, genotype}' OFS='\t' - > "$chr".tmp
awk '{print "chr"$1,$2-1,$2,$3}' OFS='\t' "$chr".tmp > "$chr".bed
"$liftOver" "$chr".bed "$hg19_hg38_chain" "${ind}_${chr}_hg38.bed" "${ind}_${chr}_hg19_unlifted.bed"
awk '{print $3,$4}' OFS='\t' "${ind}_${chr}_hg38.bed" > "${ind}_${chr}_hg38.txt"
gzip "${ind}_${chr}_hg38.txt"

mkdir -p "${evaluation_directory}/ancient_genotypes/"
mkdir -p "${evaluation_directory}/ancient_genotypes_unlifted/"

mv "${ind}_${chr}_hg38.txt.gz" "${evaluation_directory}/ancient_genotypes/"
mv "${ind}_${chr}_hg19_unlifted.bed" "${evaluation_directory}/ancient_genotypes_unlifted/"
