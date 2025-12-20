import argparse
import glob
import io
import os
import pandas as pd
import sys
import traceback
import tskit

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--variants', required=True, help='Tab-delimited file with two columns: chromosome and position in hg38 coordinates.')
	parser.add_argument('--chr', required=True, help='Chromosome to process.')
	parser.add_argument('--tree_sequences_directory', required=True, help='Directory containing .trees tree sequence files (default: current directory).')
	parser.add_argument('--output', required=True, help='Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()
	variants = pd.read_csv(args.variants, sep='\t', names=['chr', 'start', 'pos', 'ref', 'alt', 'rsID'])
	variants['pos'] = variants['pos'].astype(int)
	chr_variants = variants[variants['chr'] == args.chr]

	pos_to_age = build_position_age_map(args.chr, args.tree_sequences_directory)

	results = []
	for _, row in chr_variants.iterrows():
		pos = row['pos']
		age = pos_to_age.get(pos, None)
		if age is None:
			print(f'No age estimate found for variant at {args.chr}:{pos}', file=sys.stderr)
		results.append({
			'chr': args.chr,
			'pos': pos,
			'age_estimate': age
		})

	pd.DataFrame(results).to_csv(args.output, sep = '\t', header = False, index = False)

def retrieve_trees_files(chr_, tree_sequence_directory):
	pattern = os.path.join(tree_sequence_directory, f'hgdp_tgp_sgdp_high_cov_ancients_{chr_}_*.dated.trees')
	return sorted(glob.glob(pattern))

def build_position_age_map(chr_, tree_sequence_directory):
	pos_to_age = {}
	for ts_file in retrieve_trees_files(chr_, tree_sequence_directory):
		try:
			ts = tskit.load(ts_file)
			for site in ts.sites():
				rounded_pos = round(site.position)
				if rounded_pos not in pos_to_age:
					ages = [ts.node(m.node).time for m in site.mutations]
					if ages:
						pos_to_age[rounded_pos] = max(ages)
		except Exception as e:
			print(f"Error loading {ts_file}: Exception type: {type(e).__name__}")
			traceback.print_exc()
	return pos_to_age

if __name__ == '__main__':
	main()
