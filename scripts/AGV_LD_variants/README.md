This directory contains files used to identify TopLD variant pairs that include an AADR variant.

- identify_AGV_LD_variants.sh runs identify_AGV_LD_variants.py which retrieves TopLD variant pairs that include an AGV. Files are written per population per chromosome and output to /wynton/group/capra/projects/AADR_proxy_variants/data/AGV_LD_variants/data/'.

- calculate_proportion_TopLD_variants_in_LD_with_AGVs.sh runs calculate_proportion_TopLD_variants_in_LD_with_AGVs.py which calculates the proportion of variants in a given MAF class per population that are in LD with at least one AGV at varying LD thresholds. A file is returned per population.

- generate_summary_files.sh runs generate_summary_files.py which generates a summary file per chromosome that concatenates all the individual AGV-LD variant files across ancestry groups into a single file.
