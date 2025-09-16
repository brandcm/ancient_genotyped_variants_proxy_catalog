#!/bin/bash
#$ -N AGV_LD_variants_GWAS_intersection
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/AGV_LD_variants_GWAS_intersection.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/AGV_LD_variants/AGV_LD_variants_GWAS_intersection.err
#$ -l h_rt=2:00:00
#$ -l mem_free=10G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate basics

# assign variable
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
script="${project_directory}scripts/AGV_LD_variants/AGV_LD_variants_GWAS_intersection.py"
GWAS_directory="${project_directory}data/GWAS/"
output="${GWAS_directory}AGV_LD_variants_GWAS_intersection_summary.txt"

# run
python3 "$script" --GWAS_variants "${GWAS_directory}Aragam_et_al_2022_GCST90132314_CAD_significant_variants_hg38.txt" --GWAS_trait coronary_artery_disease --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Dand_et_al_2025_GCST90472771_psoriasis_significant_variants_hg38.txt" --GWAS_trait psoriasis --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}de_Lange_et_al_2017_GCST004133_UC_significant_variants_hg38.txt" --GWAS_trait ulcerative_colitis --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Koskeridis_et_al_2022_GCST90179150_BMI_significant_variants_hg38.txt" --GWAS_trait body_mass_index --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Mathieson_et_al_2023_NEB_significant_variants_hg38.txt" --GWAS_trait N_children_ever_born --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Suzuki_et_al_2024_T2D_significant_variants_hg38.txt" --GWAS_trait type_2_diabetes --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Trubetskoy_et_al_2022_SCZ_significant_variants_hg38.txt" --GWAS_trait schizophrenia --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Vuckovic_et_al_2020_PC_significant_variants_hg38.txt" --GWAS_trait platelet_count --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Wightman_et_al_2021_GCST013197_Alzheimers_significant_variants_hg38.txt" --GWAS_trait Alzheimers --output "$output"
python3 "$script" --GWAS_variants "${GWAS_directory}Yengo_et_al_2022_GCST90245992_height_significant_variants_hg38.txt" --GWAS_trait height --output "$output"