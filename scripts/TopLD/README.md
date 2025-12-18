This directory contains files used to download the TopLD data and calculate summary statistics.

- `retrieve_TopLD_files.sh` downloads the LD and annotation files from the SNV subdirectory for each ancestry group. This should be run on a data transfer or dev node as `bash retrieve_TopLD_files.sh`.

- `calculate_N_unique_TopLD_variants.sh` implements `calculate_N_unique_TopLD_variants.py` to return the total number of unique variants in TopLD among all four ancestry groups. The number is written to the standard out.

- `calculate N_TopLD_variants_per_ancestry_group_per_MAF_class.sh` implements `calculate N_TopLD_variants_per_ancestry_group_per_MAF_class.py` to calculate the proportion of variants belonging to four minor allele frequency classes (ultra-rare, rare, low-frequency, and common) per ancestry group in TopLD.
