#!/bin/bash
#$ -N retrieve_AGV_genotypes
#$ -t 1-3
#$ -M colin.brand@ucsf.edu
#$ -m ae
#$ -cwd
#$ -o /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/allele_frequency_trajectories/retrieve_AGV_genotypes.out
#$ -e /wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/scripts/allele_frequency_trajectories/retrieve_AGV_genotypes.err
#$ -l h_rt=2:00:00
#$ -l mem_free=20G

# load conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate EIG

# assign variables
project_directory="/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/"
config_header="${project_directory}data/allele_frequency_trajectories/config_header.txt"
variants="${project_directory}data/allele_frequency_trajectories/example_variants_for_allele_history_visualization.txt"
chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $1}' "$variants")
numeric_chr=$(awk -v row=$SGE_TASK_ID 'NR == row {print $2}' "$variants")
pos=$(awk -v row=$SGE_TASK_ID 'NR == row {print $3}' "$variants")
ref=$(awk -v row=$SGE_TASK_ID 'NR == row {print $4}' "$variants")
alt=$(awk -v row=$SGE_TASK_ID 'NR == row {print $5}' "$variants")

# make temporary directory
temp_dir=$(mktemp -d "./temp_dir.XXXXXX")

# check if tmp dir was created
if [[ ! "$temp_dir" || ! -d "$temp_dir" ]]; then
  echo "Could not create temp dir"
  exit 1
fi

# clean up function
function cleanup {
  rm -rf "$temp_dir"
  echo "Deleted temporary working directory $temp_dir"
}

trap cleanup EXIT

# change into temp directory
cd "$temp_dir"

# create config file and extract AADR genotypes
cp "$config_header" config.par
echo "chrom: $numeric_chr" >> config.par
echo "lopos: $pos" >> config.par
echo "hipos: $pos" >> config.par
echo 'genooutfilename: target.geno' >> config.par
echo 'snpoutfilename: target.snp' >> config.par
echo 'indoutfilename: target.ind' >> config.par
convertf -p config.par

# switch conda environments
conda deactivate
conda activate jupyter

# assign variables
script="${project_directory}scripts/allele_frequency_trajectories/filter_and_annotate_genotypes.py"
annotation_file="${project_directory}data/allele_frequency_trajectories/sample_annotation.txt"

# filter genotypes and visualize allele frequency
python3 "$script" --annotation_file "$annotation_file" --genotypes target.geno --output "$chr"_"$pos".frq
mv "$chr"_"$pos".frq "${project_directory}data/allele_frequency_trajectories/"
cd "${project_directory}data/allele_frequency_trajectories/"
