# 07/13/25, Colin M. Brand, University of California San Francisco

import argparse
import pandas as pd
import sys
from collections import defaultdict
from pathlib import Path

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--mismatch_output_directory', type = str, required = True, help = 'Path to mismatch output directory.')
	parser.add_argument('--output', type = str, required = True, help = 'Path to output file.')
	args = parser.parse_args()
	return args

def main() -> None:
	args = parse_args()

	samples = ['Loschbour', 'Ust_Ishim']
	chrs = [f'chr{i}' for i in range(1, 23)] + ['chrX']
	mismatch_dict: dict = defaultdict(dict)

	for sample in samples:
		for chr_ in chrs:
			filename = f'{sample}_{chr_}_minimum_R2_0.9_mismatches.txt'
			path = Path(args.mismatch_output_directory) / filename
			print(path)
			if path.exists():
				process_mismatches(path, sample, mismatch_dict)
			else:
				print(f'Warning: {filename} not found', file=sys.stderr)

	write_merged_bed(mismatch_dict, args.output)


def process_mismatches(path: Path, sample: str, bed_data: dict) -> None:
	"""Update `bed_data` dict with info from one mismatch file."""
	with open(path, 'r') as f:
		for line in f:
			fields = line.strip().split()
			if len(fields) < 20 or fields[0] != 'AGV':
				continue
			chr_ = fields[2][:-1]
			pos = int(fields[12])
			expected_gt = fields[13][:-1].split('/')
			observed_gt = fields[19][:-1].split('/')
			category = classify_match(expected_gt, observed_gt)
			key = (chr_, pos - 1, pos)
			bed_data[key][sample] = category


def write_merged_bed(bed_data: dict, out_path: str) -> None:
	with open(out_path, 'w') as out:
		for (chr_, start, end), info in sorted(bed_data.items()):
			tag = ", ".join(f"{s}: {info[s]}" for s in sorted(info))
			out.write(f"{chr_}\t{start}\t{end}\t{tag}\n")

def classify_match(expected: list[str], observed: list[str]) -> str:
	"""Return 'partial' if ≥1 allele matches, else 'complete'."""
	return 'partial' if any(a in expected for a in observed) else 'complete'

if __name__ == "__main__":
	main()
