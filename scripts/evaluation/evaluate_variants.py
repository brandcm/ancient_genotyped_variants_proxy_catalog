import argparse
import gzip
import re

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--LD_file', type=str, required=True, help='Path to file with LD information.')
	parser.add_argument('--evaluation_variants', type=str, required=True, help='Path to file with evaluation variants.')
	parser.add_argument('--LD_threshold', type=float, required=True, help='Minimum LD threshold for evaluation.')
	parser.add_argument('--output_mismatch', type=str, required=True, help='Path to output file.')
	parser.add_argument('--output_stats', type=str, required=True, help='Path to stats file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	# Set counters
	AGV_LD_variant_pairs_evaluated = 0
	partial_matches = 0
	complete_matches = 0

	# read in evaluation variants
	evaluation_dict = {}
	with gzip.open(args.evaluation_variants, 'rt') as evaluation_variants:
		for line in evaluation_variants:
			fields = line.strip().split('\t')
			pos = fields[0]
			alleles = set(fields[1].split(','))
			evaluation_dict[pos] = alleles

	# read in LD variants
	with gzip.open(args.LD_file, 'rt') as LD_file, open(args.output_mismatch, 'w') as mismatch_out:
		chr_str = re.search(r'chr(?:\d+|X|Y)', args.LD_file)
		chr = chr_str.group(0) if chr_str else None

		for line in LD_file:
			fields = line.strip().split('\t')
			AGV = fields[0]
			AGV_pos, AGV_ref, AGV_alt = AGV.split(':')
			LDV = fields[1]
			LDV_pos, LDV_ref, LDV_alt = LDV.split(':')
			ld = float(fields[2])
			corr = fields[3]

			# skip variants below LD threshold
			if ld < args.LD_threshold:
				continue

			# skip indels
			if len(AGV_ref) != 1 or len(AGV_alt) != 1 or len(LDV_ref) != 1 or len(LDV_alt) != 1:
				continue

			# allele mapping based on corr
			if corr == '+':
				AGV_to_LDV = {AGV_ref: LDV_ref, AGV_alt: LDV_alt}
			elif corr == '-':
				AGV_to_LDV = {AGV_ref: LDV_alt, AGV_alt: LDV_ref}
			else:
				mismatch_out.write(f"Invalid correlation '{corr}' for AGV {AGV_pos} and LDV {LDV_pos}.\n")
				continue

			# retrieve alleles from evaluation_dict
			AGV_eval_alleles = evaluation_dict.get(AGV_pos)
			LDV_eval_alleles = evaluation_dict.get(LDV_pos)

			# Skip AGV-LDV pairs if either variants are missing
			if not AGV_eval_alleles or not LDV_eval_alleles:
				continue
			
			# Confirm that AGVs match
			if set(AGV_eval_alleles).issubset({AGV_ref, AGV_alt}):
				AGV_LD_variant_pairs_evaluated += 1

				expected_LDV_genotype = {
					AGV_to_LDV[allele]
					for allele in AGV_eval_alleles
					if allele in AGV_to_LDV
				}

				# full match
				if LDV_eval_alleles == expected_LDV_genotype:
					complete_matches += 1
					partial_matches += 1

				# partial match
				elif LDV_eval_alleles & expected_LDV_genotype:
					partial_matches += 1
					AGV_genotype = format_genotype(AGV_eval_alleles)
					expected_LDV_genotype_str = format_genotype(expected_LDV_genotype)
					observed_LDV_genotype = format_genotype(LDV_eval_alleles)
					mismatch_out.write(f"AGV at {chr}: {AGV_pos} with genotype {AGV_genotype} maps to expected LDV at {LDV_pos} {expected_LDV_genotype_str}, but observed LDV genotype is {observed_LDV_genotype}.\n")

				# no match
				else:
					AGV_genotype = format_genotype(AGV_eval_alleles)
					expected_LDV_genotype_str = format_genotype(expected_LDV_genotype)
					observed_LDV_genotype = format_genotype(LDV_eval_alleles)
					mismatch_out.write(f"AGV at {chr}: {AGV_pos} with genotype {AGV_genotype} maps to expected LDV at {LDV_pos} {expected_LDV_genotype_str}, but observed LDV genotype is {observed_LDV_genotype}.\n")

	# Write stats to output
	with open(args.output_stats, 'a') as stats_out:
		stats_out.write(f"{args.LD_threshold}\t{chr}\t{partial_matches}\t{complete_matches}\t{AGV_LD_variant_pairs_evaluated}\n")

def format_genotype(alleles):
	"""Format genotype for display."""
	return '/'.join(sorted(alleles) * 2 if len(alleles) == 1 else sorted(alleles))

if __name__ == '__main__':
	main()
