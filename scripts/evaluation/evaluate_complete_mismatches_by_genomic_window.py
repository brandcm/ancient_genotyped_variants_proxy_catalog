import argparse
import gzip
import re
import math
from collections import defaultdict

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--LD_file', type=str, required=True, help='Path to file with LD information.')
	parser.add_argument('--evaluation_variants', type=str, required=True, help='Path to file with evaluation variants.')
	parser.add_argument('--LD_threshold', type=float, required=True, help='Minimum LD threshold for evaluation.')
	parser.add_argument('--window_size', type=int, default=50_000, help='Window size in base pairs (default: 50 kb)')
	parser.add_argument('--step_size', type=int, default=25_000, help='Step size between windows (default: 25 kb)')
	parser.add_argument('--output', type=str, required=True, help='Path to output file with mismatchs per window.')
	return parser.parse_args()

def main():
	args = parse_args()

	mismatch_by_window = defaultdict(lambda: {'mismatches': 0, 'total': 0})
	max_pos = 0
	N_mismatched_AGVs_by_window = defaultdict(set)

	chr_str = re.search(r'chr(?:\d+|X|Y)', args.LD_file)
	chr_ = chr_str.group(0) if chr_str else 'chr?'

	# read in evaluation variants
	evaluation_dict = {}
	with gzip.open(args.evaluation_variants, 'rt') as evaluation_file:
		for line in evaluation_file:
			fields = line.strip().split('\t')
			pos = fields[0]
			alleles = set(fields[1].split(','))
			evaluation_dict[pos] = alleles

	with gzip.open(args.LD_file, 'rt') as LD_file:
		for line in LD_file:
			fields = line.strip().split('\t')
			AGV = fields[0]
			AGV_pos, AGV_ref, AGV_alt = AGV.split(':')
			LDV = fields[1]
			LDV_pos, LDV_ref, LDV_alt = LDV.split(':')
			ld = float(fields[2])
			corr = fields[3]

			if ld < args.LD_threshold:
				continue

			if len(AGV_ref) != 1 or len(AGV_alt) != 1 or len(LDV_ref) != 1 or len(LDV_alt) != 1:
				continue

			if corr == '+':
				AGV_to_LDV = {AGV_ref: LDV_ref, AGV_alt: LDV_alt}
			elif corr == '-':
				AGV_to_LDV = {AGV_ref: LDV_alt, AGV_alt: LDV_ref}
			else:
				continue

			AGV_eval_alleles = evaluation_dict.get(AGV_pos)
			LDV_eval_alleles = evaluation_dict.get(LDV_pos)
			if not AGV_eval_alleles or not LDV_eval_alleles:
				continue

			if not set(AGV_eval_alleles).issubset({AGV_ref, AGV_alt}):
				continue

			expected_LDV_genotype = {
				AGV_to_LDV[allele]
				for allele in AGV_eval_alleles
				if allele in AGV_to_LDV
			}

			max_pos = max(max_pos, int(AGV_pos), int(LDV_pos))

			positions = [int(AGV_pos), int(LDV_pos)]

			mismatched = LDV_eval_alleles != expected_LDV_genotype and not LDV_eval_alleles & expected_LDV_genotype
			for pos in positions:
				window_starts = get_window_starts(pos, args.window_size, args.step_size)
				for window_start in window_starts:
					key = (chr_, window_start)
					mismatch_by_window[key]['total'] += 1
					if mismatched:
						mismatch_by_window[key]['mismatches'] += 1
						N_mismatched_AGVs_by_window[key].add(AGV)

	with open(args.output, 'w') as out:
		for pos in range(0, max_pos + 1, args.step_size):
			key = (chr_, pos)
			window_start = pos + 1
			window_end = pos + args.window_size

			stats = mismatch_by_window.get(key, {'mismatches': 0, 'total': 0})
			mismatches = stats['mismatches']
			total = stats['total']

			N_mismatched_AGVs = len(N_mismatched_AGVs_by_window.get(key, set()))
			out.write(f"{chr_}\t{window_start}\t{N_mismatched_AGVs}\t{mismatches}\t{total}\n")

def get_window_starts(pos, window_size, step_size):
	"""Return all window starts that a position belongs to."""
	starts = []
	first = ((pos - window_size) // step_size + 1) * step_size
	last = (pos // step_size) * step_size
	for s in range(first, last + 1, step_size):
		if s >= 0:
			starts.append(s)
	return starts

def format_genotype(alleles):
	"""Format genotype for display."""
	return '/'.join(sorted(alleles) * 2 if len(alleles) == 1 else sorted(alleles))

if __name__ == '__main__':
	main()
