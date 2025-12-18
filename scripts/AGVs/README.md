This directory contains files used to retrieve data on the ancient genotyped variants. Scripts are listed in the order in which they should be run.

- `retrieve_and_format_AGVs.sh` generates BED files of the AGVs using both the hg19 and hg38 assemblies. Differences in reference allele are corrected in the hg38 BED file using the `check_reference_bases_in_AGVs_hg38_BED.py` script as liftOver does not update allele information. This script switches the reference and alternate allele in hg38 for sites where the hg19 and hg38 reference alleles do not match. The rsID and different reference alleles are also printed to the standard out as a record of updates made to the hg38 BED file.

- `create_AGVs_hg38_dictionary.py` generates a pickle where chromosomes are keys and the values are colon-delimited strings with the position, reference allele, and alternate allele. Run on the command line using `python3 create_AGVs_hg38_dictionary.py`.

- `retrieve_AGV_gnomAD_allele_frequencies.sh` retrieves gnomAD v4.1 allele frequencies for all, AFR, EAS, NFE, and SAS ancestry groups. These frequencies are placed in a new subdirectory in the `data/AGVs/` directory.

- `AGVs_TopLD_presence_summary.sh` implements `AGVs_TopLD_presence_summary.py` to retrieve metadata per AGV: 1) presence in TopLD ancestry groups, 2) minor allele frequency in TopLD, and 3) presence in LD with $\geq$ one variant in TopLD.

- `annotate_AGVs.sh` implements `annotate_AGVs.py` to merge gnomAD allele frequencies with the TopLD annotations per AGV.

- `quantify_ancient_sample_coverge_per_site.sh` implements `quantify_ancient_sample_coverge_per_site.py` to quantify the number of ancient samples in the AADR that are genotyped at a given AGV.

- `concat_ancient_sample_coverage_per_site.sh` concatenates the chromosome-level outputs from the above script.
