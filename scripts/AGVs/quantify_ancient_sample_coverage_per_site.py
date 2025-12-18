import gzip
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--VCF', type = str, required = True, help = 'Path to input VCF.')
	parser.add_argument('--output', type = str, required = True, help = 'Path to output file.')
	args = parser.parse_args()
	return args

def main() -> None:
	args = parse_args()

	assess_ancient_sample_coverage(args.VCF, args.output)

def assess_ancient_sample_coverage(VCF_path, output_path):
	open_in = gzip.open if VCF_path.endswith('.gz') else open
	open_out = gzip.open if output_path.endswith('.gz') else open

	with open_in(VCF_path, 'rt') as VCF, open_out(output_path, 'wt') as out:
		for line in VCF:
			if line.startswith('##'):
				continue
			elif line.startswith('#CHROM'):
				out.write('chr\tpos\tnon_missing_samples\n')
				continue

			fields = line.strip().split('\t')
			chr_, pos = fields[0], fields[1]
			ancient_samples = fields[9:9999 + 1]  # First 9990 samples
			non_missing = sum(1 for field in ancient_samples if is_non_missing(field))
			out.write(f'{chr_}\t{pos}\t{non_missing}\n')

def is_non_missing(gt_field):
	gt = gt_field.split(':')[0]
	return gt not in ['./.', '.']

if __name__ == "__main__":
	main()
