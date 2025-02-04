This directory contains files used to retrieve allele age estimates from the Human Genome Dating project. Scripts are listed in the order in which they should be run.

- retrieve_HGD_gnomAD_allele_frequencies.sh retrieves global allele frequencies from gnomAD v2.1.1 for all variants that have a "PASS" filter in the HGD and places frequencies in a new subdirectory in the data/AGV_age_estimates/ directory.

- retrieve_HGD_AGVs.sh retrieves age estimate information for AGVs present in the HGD dataset and maps allele frequencies from gnomAD (generated above) to each variant using the `map_gnomAD_AFs.py` script.

- concat_AGVs_with_age_estimates_and_AFs.sh concatenates the individual chromosome-level outputs from above into a single file.

- generate_allele_frequency_matched_random_sample_for_AGV_age_estimates.sh implements generate_allele_frequency_matched_random_sample_for_AGV_age_estimates.py to generate a random sample of allele ages from the Human Genome Dating project that matches on allele frequency bin and the distribution of data sources (Combined, Simons Genome Diversity Project, Thousand Genomes).