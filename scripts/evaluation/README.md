This directory contains scripts to download and evaluate proxy variants in two high-coverage ancient human genomes.

- `filter_AGV_LD_variant_files_for_evaluation.sh` subsets the EUR AGV-LD variant pairs where all alleles are SNVs and r-squared $\geq$ 0.5. This script can be run concurrent with the script immediately below.

- `filter_and_liftOver_high_quality_evaluation_variants.sh` filters variants based on site quality for Loschbour and Ust-Ishim and then generates a tab-delimited alleles files where the alleles for each position are listed in hg38 coordinates after liftOver from hg19.

- `evaluate_variants.sh` implements `evaluate_variants.py` to assess many AGV-LD variant pairs are partially or completely correct in the ancient genomes. This script generates a per sample per LD threshold per chromosome mismatch file that notes when the prediction was not correct as well as a per sample overall summary file with the number of correct partial and complete matches.
