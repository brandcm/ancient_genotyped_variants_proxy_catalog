import argparse
import os
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--effect_loci_file', type = str, required = True, help = 'Path to effect loci file formatted as a tab-delimited file where chr and rsID are the fields.')
	parser.add_argument('--AGV_LD_variant_directory', type = str, required = True, help = 'Path to AGV-LD variant directory.')
	parser.add_argument('--output', type = str, required = True, help = 'Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	map_AGVs_or_proxies(
		rsIDs_file=args.effect_loci_file,
		AGV_LD_variant_directory=args.AGV_LD_variant_directory,
		output_file=args.output
	)

def map_AGVs_or_proxies(rsIDs_file, AGV_LD_variant_directory, output_file):
	"""
	Map each variant to itself if it is an AGV, else find a proxy with highest r2 in EUR.
	"""
	min_r2_threshold = 0.5

	rsIDs_df = pd.read_csv(rsIDs_file, sep='\t', header=None, names=['chr','rsID','effect_allele','other_allele','GWAS_beta','GWAS_p_value'])
	AGVs_df = pd.read_csv('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/AGVs_hg38.bed', sep='\t', names=['chr','start','end','ref','alt','rsID'])

	AGV_rsIDs_set = set(AGVs_df['rsID'])
	mapped_rows = []

	LD_cache = {}

	for _, row in rsIDs_df.iterrows():
		variant_chr = row['chr']
		variant_rsID = str(row['rsID']).strip()
		GWAS_beta = float(row['GWAS_beta'])
		GWAS_p_value = float(row['GWAS_p_value'])
		effect_allele = row['effect_allele']
		other_allele = row['other_allele']

		if GWAS_beta > 0:
			trait_increasing_allele = effect_allele
		elif GWAS_beta < 0:
			trait_increasing_allele = other_allele
		else:
			trait_increasing_allele = None

		if variant_chr not in LD_cache:
			LD_file = os.path.join(AGV_LD_variant_directory, f"{variant_chr}_AGV_LDVs_summary.txt.gz")
			LD_columns = ['chr', 'AGV', 'AGV_rsID', 'LDV', 'LDV_rsID', 'r2', "D'", 'corr', 'populations']
			LD_df = pd.read_csv(LD_file, sep='\t', header=None, names=LD_columns, compression='gzip')
			LD_df = LD_df[LD_df['populations'].str.contains('EUR', na=False)]
			LD_cache[variant_chr] = LD_df
		else:
			LD_df = LD_cache[variant_chr]

		if variant_rsID in AGV_rsIDs_set:
			mapped_rows.append({
				'chr': variant_chr,
				'GWAS_rsID': variant_rsID,
				'GWAS_beta': GWAS_beta,
				'GWAS_p_value': GWAS_p_value,
				'AGV_rsID': variant_rsID,
				'proxy': False,
				'r2': None,
				'AGV_trait_increasing_allele': trait_increasing_allele
			})
		else:
			candidates = LD_df[LD_df['LDV_rsID'].astype(str).str.strip() == variant_rsID].copy()
			if not candidates.empty:
				candidates['r2_EUR'] = candidates.apply(lambda row: extract_EUR_r2(row['populations'], row['r2']), axis=1)
				candidates['corr_EUR'] = candidates.apply(lambda r: extract_EUR_corr(r['populations'], r['corr']), axis=1)
				candidates = candidates[candidates['r2_EUR'] >= min_r2_threshold]

			if candidates.empty:
				mapped_rows.append({
					'chr': variant_chr,
					'GWAS_rsID': variant_rsID,
					'GWAS_beta': GWAS_beta,
					'GWAS_p_value': GWAS_p_value,
					'AGV_rsID': None,
					'proxy': False,
					'r2': None,
					'AGV_trait_increasing_allele': None
				})
			else:
				best = candidates.loc[candidates['r2_EUR'].idxmax()]

				AGV_pos, AGV_ref, AGV_alt = best['AGV'].split(':')
				LDV_pos, LDV_ref, LDV_alt = best['LDV'].split(':')

				corr_EUR = best['corr_EUR']
				if corr_EUR == '+':
					LDV_to_AGV = {LDV_ref: AGV_ref, LDV_alt: AGV_alt}
				elif corr_EUR == '-':
					LDV_to_AGV = {LDV_ref: AGV_alt, LDV_alt: AGV_ref}

				linked_trait_increasing_allele = LDV_to_AGV.get(trait_increasing_allele, None)

				mapped_rows.append({
					'chr': variant_chr,
					'GWAS_rsID': variant_rsID,
					'GWAS_beta': GWAS_beta,
					'GWAS_p_value': GWAS_p_value,
					'AGV_rsID': best['AGV_rsID'],
					'proxy': True,
					'r2': best['r2_EUR'],
					'AGV_trait_increasing_allele': linked_trait_increasing_allele
				})

	mapped_df = pd.DataFrame(mapped_rows)
	mapped_df.to_csv(output_file, sep='\t', index=False)

def extract_EUR_r2(pop_str, r2_str):
	pops = [p.strip() for p in pop_str.split(',')]
	r2s = [float(r.strip()) for r in r2_str.split(',')]
	for i, pop in enumerate(pops):
		if pop == 'EUR':
			return r2s[i]
	return None

def extract_EUR_corr(pop_str, corr_str):
	pops = [p.strip() for p in pop_str.split(',')]
	corrs = [c.strip() for c in corr_str.split(',')]
	for i, pop in enumerate(pops):
		if pop == 'EUR':
			return corrs[i]
	return None

if __name__ == "__main__":
	main()