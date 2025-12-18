#!/bin/bash
#$ -N liftOver_GWAS_to_hg38
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/liftOver_GWAS_to_hg38.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/liftOver_GWAS_to_hg38.err
#$ -l h_rt=1:00:00
#$ -l mem_free=10G

# assign variables
liftOver="/wynton/group/capra/bin/liftOver/liftOver"
hg19_hg38_chain="/wynton/group/capra/bin/liftOver/hg19ToHg38.over.chain.gz"

# change directories
cd /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/GWAS

# run
"$liftOver" Mathieson_et_al_2023_NEB_significant_variants_hg19.bed "$hg19_hg38_chain" Mathieson_et_al_2023_NEB_significant_variants_hg38.bed Mathieson_et_al_2023_NEB_significant_variants_hg19_unlifted.bed
awk '{print $1,$3}' OFS='\t' Mathieson_et_al_2023_NEB_significant_variants_hg38.bed > Mathieson_et_al_2023_NEB_significant_variants_hg38.txt 

"$liftOver" Suzuki_et_al_2024_T2D_significant_variants_hg19.bed "$hg19_hg38_chain" Suzuki_et_al_2024_T2D_significant_variants_hg38.bed Suzuki_et_al_2024_T2D_significant_variants_hg19_unlifted.bed
awk '{print $1,$3}' OFS='\t' Suzuki_et_al_2024_T2D_significant_variants_hg38.bed > Suzuki_et_al_2024_T2D_significant_variants_hg38.txt

"$liftOver" Trubetskoy_et_al_2022_SCZ_significant_variants_hg19.bed "$hg19_hg38_chain" Trubetskoy_et_al_2022_SCZ_significant_variants_hg38.bed Trubetskoy_et_al_2022_SCZ_significant_variants_hg19_unlifted.bed
awk '{print $1,$3}' OFS='\t' Trubetskoy_et_al_2022_SCZ_significant_variants_hg38.bed > Trubetskoy_et_al_2022_SCZ_significant_variants_hg38.txt

"$liftOver" Wightman_et_al_2021_GCST013197_Alzheimers_significant_variants_hg19.bed "$hg19_hg38_chain" Wightman_et_al_2021_GCST013197_Alzheimers_significant_variants_hg38.bed Wightman_et_al_2021_GCST013197_Alzheimers_significant_variants_hg19_unlifted.bed
awk '{print $1,$3}' OFS='\t' Wightman_et_al_2021_GCST013197_Alzheimers_significant_variants_hg38.bed > Wightman_et_al_2021_GCST013197_Alzheimers_significant_variants_hg38.txt