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
	# -----------------------------
	# Load data
	# -----------------------------
	rsIDs_df = pd.read_csv(rsIDs_file, sep='\t', header=None, names=['chr','rsID','effect_allele','other_allele','GWAS_beta'])
	AGVs_df = pd.read_csv('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/AGVs_hg38.bed', sep='\t', names=['chr','start','end','ref','alt','rsID'])

	AGV_rsIDs_set = set(AGVs_df['rsID'])
	mapped_rows = []

	LD_cache = {}

	for _, row in rsIDs_df.iterrows():
		variant_chr = row['chr']
		variant_rsID = str(row['rsID']).strip()
		GWAS_beta = row['GWAS_beta']
		effect_allele = row['effect_allele']
		print(variant_rsID)

		if variant_chr not in LD_cache:
			LD_file = os.path.join(AGV_LD_variant_directory, f"{variant_chr}_AGV_LDVs_summary.txt.gz")
			LD_columns = ['chr', 'AGV', 'AGV_rsID', 'LDV', 'LDV_rsID', 'r2', "D'", 'corr', 'populations']
			LD_df = pd.read_csv(LD_file, sep='\t', header=None, names=LD_columns, compression='gzip')
			print(LD_df.iloc[0])
			LD_df = LD_df[LD_df['populations'].str.contains('EUR', na=False)]
			LD_cache[variant_chr] = LD_df
		else:
			LD_df = LD_cache[variant_chr]

		if variant_rsID in AGV_rsIDs_set:
			mapped_rows.append({
				'chr': variant_chr,
				'rsID': variant_rsID,
				'GWAS_beta': GWAS_beta,
				'AGV_rsID': variant_rsID,
				'proxy': False,
				'r2': 1.0,
				'effect_allele': effect_allele
			})
		else:
			# Variant is not an AGV → find proxy
			candidates = LD_df[LD_df['LDV_rsID'].astype(str).str.strip() == variant_rsID].copy()
			if not candidates.empty:
				candidates['r2_EUR'] = candidates.apply(lambda row: extract_r2_eur(row['populations'], row['r2']), axis=1)
				candidates = candidates[candidates['r2_EUR'] >= min_r2_threshold]

			if candidates.empty:
				mapped_rows.append({
					'chr': variant_chr,
					'rsID': variant_rsID,
					'GWAS_beta': GWAS_beta,
					'AGV_rsID': None,
					'proxy': False,
					'r2': None,
					'effect_allele': None
				})
			else:
				best = candidates.loc[candidates['r2_EUR'].idxmax()]

				# Parse AGV and LDV alleles
				AGV_pos, AGV_ref, AGV_alt = best['AGV'].split(':')
				LDV_pos, LDV_ref, LDV_alt = best['LDV'].split(':')

				# Build allele mapping depending on corr
				if best['corr'] == '+':
					LDV_to_AGV = {LDV_ref: AGV_ref, LDV_alt: AGV_alt}
				else:
					LDV_to_AGV = {LDV_ref: AGV_alt, LDV_alt: AGV_ref}

				# Map proxy effect allele to AGV allele
				linked_effect_allele = LDV_to_AGV.get(effect_allele, None)

				mapped_rows.append({
					'chr': variant_chr,
					'rsID': variant_rsID,
					'GWAS_beta': GWAS_beta,
					'AGV_rsID': best['AGV_rsID'],
					'proxy': True,
					'r2': best['r2_EUR'],
					'effect_allele': linked_effect_allele
				})

	mapped_df = pd.DataFrame(mapped_rows)
	mapped_df.to_csv(output_file, sep='\t', index=False)
	print(f"Saved AGV/proxy mapping to {output_file}")

def extract_r2_eur(pop_str, r2_str):
	pops = [p.strip() for p in pop_str.split(',')]
	r2s = [float(r.strip()) for r in r2_str.split(',')]
	for i, pop in enumerate(pops):
		if pop == 'EUR':
			return r2s[i]
	return None

if __name__ == "__main__":
	main()