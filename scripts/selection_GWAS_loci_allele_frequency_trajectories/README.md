This directory contains files used to characterize allele frequencies of GWAS hits under putative directional selection. Note that the directional selection datasets must be downloaded manually and renamed: `/data/selection/Akbari_et_al_2024_hg19.txt.gz` can be retrieved from [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7RVV9N) and `data/selection/Irving_Pease_et_al_2024_hg19.txt.gz` is Table S2.1.4 from this [paper](https://www.nature.com/articles/s41586-023-06705-1).

- `retrieve_selection_loci.sh` filters the Akbari et al. 2024 and Irving-Pease et al. 2024 selection datasets for significant loci only. This should be run on a dev node as `bash retrieve_selection_loci.sh`.

- `liftOver_selection_loci.sh` converts the significant selection loci from hg19 to hg38 coordinates. This should be run on a dev node as `bash liftOver_selection_loci.sh`.

- `retrieve_significant_GWAS_loci.sh` retrieves significant GWAS loci for two complex traits: BMI and height. This should be run on a data transfer or dev node as `bash retrieve_significant_GWAS_loci.sh`.

After these three scripts have completed, run all cells in the "Selection GWAS Loci Allele Frequency Trajectories" section of the [analysis notebook](https://github.com/brandcm/ancient_genotyped_variants_proxy_catalog/blob/main/scripts/notebooks/analysis.ipynb). This will run the intersection and generate the outputs to complete the following scripts that analyze effects by the top 20% of loci with 1) the largest absolute beta and 2) the strongest (i.e., lowest) p-values.

- `identify_selection_GWAS_*_loci_proxies.sh` implements `identify_selection_GWAS_*_loci_proxies.py` assesses which variants are AGVs and which variants require a proxy, selecting the linked variant with the highest r2 in the EUR ancestry group for non-AGVs.

- `retrieve_selection_GWAS_*_loci_proxy_AFs.sh` implements `retrieve_selection_GWAS_*_loci_proxy_AFs.py` to retrieve allele frequencies for the proxy variants identified above.

- `concat_selection_GWAS_*_loci_proxy_AFs.sh` concatenates the chromosome-level allele frequencies from above.