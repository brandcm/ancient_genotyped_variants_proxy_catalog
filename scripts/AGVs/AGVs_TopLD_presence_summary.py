import argparse
import os
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--AGVs_BED', type=str, required=True, help='Path to AGVs hg38 BED file.')
	parser.add_argument('--chr', type=str, required=True, help='Chromosome for which to assess AGV presence in TopLD.')
	parser.add_argument('--TopLD_directory', type=str, required=True, help='Path to TopLD directory.')
	parser.add_argument('--AGV_LD_variants_directory', type=str, required=True, help='Path to directory with AGV-LD variant pairs.')
	parser.add_argument('--output', type=str, required=True, help='Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	AGVs_TopLD_presence_summary(args.AGVs_BED, args.chr, args.TopLD_directory, args.AGV_LD_variants_directory, args.output)

def AGVs_TopLD_presence_summary(AGVs_BED, chr, TopLD_directory, AGV_LD_variants_directory, output):
	"""
	Parses a BED file and summarizes variant presence in TopLD and whether such variants are in LD with other modern variants.

	Parameters:
	- AGVs_BED (str): Path to the 1240K hg38 BED file.
	- chr (str): Chromosome for which to assess AGV presence.
	- TopLD_directory (str): Path to TopLD directory.
	- AGV_LD_variants_directory (str): Path to directory with AGV-LD variant pairs.

	Output:
	- A text file with chr, pos, and a comma-delimited lists of:
	1) ancestry group presence in TopLD
	2) MAFs for ancestry group presence
	3) ancestry groups where the variant occurs in LD with at least one other variant
	"""
	AGVs_df = pd.read_csv(AGVs_BED, sep='\t', header=None, names=['chr','start','end','ref','alt','rsID'])
	AGVs_df['ID'] = AGVs_df['end'].astype(str) + ':' + AGVs_df['ref'] + ':' + AGVs_df['alt']

	ancestry_groups = ['AFR', 'EAS', 'EUR', 'SAS']
	results_dict = {}

	chr_subset_AGVs_df = AGVs_df[AGVs_df['chr'] == chr]

	for ancestry_group in ancestry_groups:
		annotation_path = os.path.join(TopLD_directory, f'{ancestry_group}_{chr}_no_filter_0.2_1000000_info_annotation.csv.gz')

		if not os.path.isfile(annotation_path):
			print(f"Warning: File '{annotation_path}' does not exist. Skipping ancestry group {ancestry_group} for chromosome {chr}.")
			continue

		annotation_df = pd.read_csv(annotation_path, sep=',', header=0, usecols=['Uniq_ID','MAF'])
		merged_df = pd.merge(chr_subset_AGVs_df, annotation_df, left_on='ID', right_on='Uniq_ID', how='left')
		TopLD_ancestry_groups = merged_df.dropna(subset=['MAF'])

		LD_file_path = os.path.join(AGV_LD_variants_directory, f'{ancestry_group}_{chr}_AGV_LD_variants.txt.gz')

		LD_ancestry_groups = []
		if os.path.isfile(LD_file_path):
			LD_df = pd.read_csv(LD_file_path, sep='\t', names=['chr','AGV','LDV','rsID','R2','D\'','corr'])
			AGVs_in_LD = set(LD_df['AGV'].values)

			for _, row in TopLD_ancestry_groups.iterrows():
				variant_id = row['ID']
				matching_AGVs = set([variant_id]) & AGVs_in_LD

				if matching_AGVs:
					LD_ancestry_groups.append(ancestry_group)
					break

		for _, row in TopLD_ancestry_groups.iterrows():
			variant_key = (row['chr'], row['end'])

			if variant_key not in results_dict:
				results_dict[variant_key] = {
					'ancestry_groups_present_in_TopLD': [],
					'TopLD_MAFs': [],
					'ancestry_groups_with_LDVs': []
				}

			rounded_MAF = round(row['MAF'], 3)

			results_dict[variant_key]['ancestry_groups_present_in_TopLD'].append(ancestry_group)
			results_dict[variant_key]['TopLD_MAFs'].append(str(rounded_MAF))
			results_dict[variant_key]['ancestry_groups_with_LDVs'].extend(LD_ancestry_group)

	with open(output, 'w') as out:
		for (chr, pos), data in results_dict.items():
			matching_row = AGVs_df[(AGVs_df['chr'] == chr) & (AGVs_df['end'] == pos)]
			if not matching_row.empty:
				ref = matching_row['ref'].iloc[0]
				alt = matching_row['alt'].iloc[0]
			else:
				continue
				
			join_ID = f"{chr}_{pos}_{ref}_{alt}"

			ancestry_group_order = ['AFR', 'EAS', 'EUR', 'SAS']
			sorted_ancestry_groups = sorted(set(data['ancestry_groups_present_in_TopLD']), key=lambda x: ancestry_group_order.index(x))
			sorted_MAFs = [data['TopLD_MAFs'][data['ancestry_groups_present_in_TopLD'].index(ancestry_group)] for ancestry_group in sorted_ancestry_groups]
			sorted_LD_ancestry_groups = sorted(set(data['ancestry_groups_with_LDVs']), key=lambda x: ancestry_group_order.index(x))

			out.write(f"{join_ID}\t{','.join(sorted_ancestry_groups)}\t{','.join(sorted_MAFs)}\t{','.join(sorted_LD_ancestry_groups)}\n")

if __name__ == '__main__':
	main()