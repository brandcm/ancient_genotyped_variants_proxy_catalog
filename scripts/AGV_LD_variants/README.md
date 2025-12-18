This directory contains files used to identify TopLD variant pairs that include an AADR variant.

- `identify_AGV_LD_variants.sh` implements `identify_AGV_LD_variants.py` to retrieve TopLD variant pairs that include an AGV. Files are written per population per chromosome and output to `/wynton/group/capra/projects/AADR_proxy_variants/data/AGV_LD_variants/data/`.

- `calculate_proportion_TopLD_variants_in_LD_with_AGVs.sh` implements `calculate_proportion_TopLD_variants_in_LD_with_AGVs.py` to calculate the proportion of variants in a given MAF class per population that are in LD with at least one AGV at varying LD thresholds. A file is returned per population.

- `generate_summary_files.sh` implements `generate_summary_files.py` to generate a summary file per chromosome that concatenates all the individual AGV-LD variant files across ancestry groups into a single file.

- `liftOver_GWAS_to_hg38.sh` converts any GWAS using the hg19 reference to the hg38 reference for the subsequent script.

- `AGV_LD_variants_GWAS_intersetion.sh` implements `AGV_LD_variants_GWAS_intersetion.py` to quantify how many AGVs and AGVs plus linked variants are recovered in ten GWAS.