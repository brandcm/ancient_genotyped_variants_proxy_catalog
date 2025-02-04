import argparse
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--AGV_LD_variants_directory', type=str, required=True, help='Path to directory with AGV-LD variant pairs.')
	parser.add_argument('--chromosome', type=str, required=True, help='Target chromosome.')
	parser.add_argument('--TopLD_directory', type=str, required=True, help='Path to TopLD directory.')
	parser.add_argument('--out', type=str, required=True, help='Path to output file.')
	args=parser.parse_args()
	return args

def main():
	args = parse_args()

	# Load dataframes per population
	AFR_df = pd.read_csv(f'{args.AGV_LD_variants_directory}AFR_{args.chromosome}_AGV_LD_variants.txt.gz', sep='\t', header=None, names=['chr','AGV','LDV','rsID','R2','D\'','corr'])
	AFR_df['pops'] = 'AFR'

	EAS_df = pd.read_csv(f'{args.AGV_LD_variants_directory}EAS_{args.chromosome}_AGV_LD_variants.txt.gz', sep='\t', header=None, names=['chr','AGV','LDV','rsID','R2','D\'','corr'])
	EAS_df['pops'] = 'EAS'

	EUR_df = pd.read_csv(f'{args.AGV_LD_variants_directory}EUR_{args.chromosome}_AGV_LD_variants.txt.gz', sep='\t', header=None, names=['chr','AGV','LDV','rsID','R2','D\'','corr'])
	EUR_df['pops'] = 'EUR'

	SAS_df = pd.read_csv(f'{args.AGV_LD_variants_directory}SAS_{args.chromosome}_AGV_LD_variants.txt.gz', sep='\t', header=None, names=['chr','AGV','LDV','rsID','R2','D\'','corr'])
	SAS_df['pops'] = 'SAS'

	dfs = [AFR_df,EAS_df,EUR_df,SAS_df]
	merged_df = dfs[0]

	merged_df = pd.concat(dfs, axis=0, ignore_index=True)

	grouped_df = merged_df.groupby(['chr', 'AGV', 'LDV', 'rsID'], as_index=False).agg(
	{
		'R2': aggregate,
		'D\'': aggregate,
		'corr': aggregate,
		'pops': aggregate
	}
)

	grouped_df.to_csv(args.out, sep='\t', header=True, index=False, compression='gzip')

def aggregate(values):
	"""Aggregate unique values into a comma-separated string."""
	values = values.dropna().unique()
	if values.size > 0:
		return ','.join(map(str, values))
	return None

if __name__ == '__main__':
	main()
