import argparse
import gzip
import pandas as pd
from collections import defaultdict

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--AGV_LD_variants_directory', type=str, required=True, help='Path to directory with AGV-LD variant pairs.')
	parser.add_argument('--chr', type=str, required=True, help='Target chromosome.')
	parser.add_argument('--out_directory', type=str, required=True, help='Path to output file.')
	return parser.parse_args()

def main():
	args = parse_args()
	chromosome = args.chr
	ancestry_groups = ['AFR', 'EAS', 'EUR', 'SAS']
	AGV_rsID_mapping = load_AGVs_BED()
	variant_pairs = defaultdict(lambda: defaultdict(list))

	for ancestry_group in ancestry_groups:
		file_path = f"{args.AGV_LD_variants_directory}/{ancestry_group}_{chromosome}_AGV_LD_variants.txt.gz"
		try:
			with gzip.open(file_path, 'rt') as f:
				df = pd.read_csv(f, sep='\t', names=['chr', 'AGV', 'LDV', 'LDV_rsID', 'r2', 'D', 'corr'])
				df['chr'] = df['chr'].str.replace('chr', '', regex=False)

				for _, row in df.iterrows():
					key = tuple(row[['chr', 'AGV', 'LDV', 'LDV_rsID']])
					variant_pairs[key]['ancestry_groups'].append(ancestry_group)
					variant_pairs[key]['r2'].append((ancestry_group, str(row['r2'])))
					variant_pairs[key]['D'].append((ancestry_group, str(row['D'])))
					variant_pairs[key]['corr'].append((ancestry_group, str(row['corr'])))

		except FileNotFoundError:
			print(f'File not found: {file_path}')
			continue

	df_rows = []
	for key, data in variant_pairs.items():
		chr_, AGV, LDV, rsID = key

		try:
			pos, ref, alt = AGV.split(':')
		except ValueError:
			pos, ref, alt = "NA", "NA", "NA"
		AGV_rsID = AGV_rsID_mapping.get((chr_, pos, ref, alt), 'NA')

		sorted_ancestry_groups = sorted(data['ancestry_group'])
		sorted_r2 = [val for ancestry_group, val in sorted(data['r2'])]
		sorted_D = [val for ancestry_group, val in sorted(data['D'])]
		sorted_corr = [val for ancestry_group, val in sorted(data['corr'])]

		df_rows.append([
			chr_, AGV, AGV_rsID, LDV, rsID,
			','.join(sorted_r2),
			','.join(sorted_D),
			','.join(sorted_corr),
			','.join(sorted_ancestry_groups)
		])

	final_df = pd.DataFrame(df_rows, columns=['chr','AGV','AGV_rsID','LDV','LDV_rsID','ancestry_group','r2','D\'','corr'])
	final_df = final_df.sort_values(by=['AGV', 'LDV'], key=lambda x: x.map(extract_numeric))

	output_path = f'{args.out_directory}/{chromosome}_AGV_LDVs_summary.txt.gz'
	final_df.to_csv(output_path, sep='\t', index=False, compression='gzip')

def load_AGVs_BED():
	bed_df = pd.read_csv('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/AGVs_hg38.bed', sep='\t', header=None, names=['chr', 'start', 'end', 'ref', 'alt', 'rsID'])
	bed_df['chr'] = bed_df['chr'].str.replace('chr', '', regex=False)
	return {(row['chr'], str(row['end']), row['ref'], row['alt']): row['rsID'] for _, row in bed_df.iterrows()}

def extract_numeric(value):
	return int(value.split(':')[0])

if __name__ == '__main__':
	main()
