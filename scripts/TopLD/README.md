This directory contains files used to download the TopLD data and calculate summary statistics.

- retrieve_TopLD_files.sh downloads the LD and annotation files from the SNV subdirectory for each population. This should be run on a data transfer or dev node as "bash retrieve_TopLD_files.sh".

- calculate_N_unique_TopLD_variants.sh run calculate_N_unique_TopLD_variants.py which returns the total number of unique variants in TopLD among all four populations. The number is written to the std out.

- calculate N_TopLD_variants_per_population_per_MAF_class.sh runs calculate N_TopLD_variants_per_population_per_MAF_class.py which calculates the proportion of variants belonging to four minor allele frequency classes (ultra-rare, rare, low-frequency, and common) per population.
