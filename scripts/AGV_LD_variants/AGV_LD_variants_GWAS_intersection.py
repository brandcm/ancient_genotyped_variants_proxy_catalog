import argparse
import glob
import gzip
import os

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--GWAS_variants', type=str, required=True, help='File of significant variants from a GWAS. Formatted as tab-delimited chromosome and position (e.g., chr1\t123456).')
	parser.add_argument('--GWAS_trait', type=str, required=True, help='Name of GWAS trait.')
	parser.add_argument('--output', type=str, required=True, help='Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	AGV_set = generate_AGV_set()
	LD_variant_set = generate_LD_variant_set()
	LD_variant_set.update(AGV_set)

	print(len(AGV_set))
	print(len(LD_variant_set))

	N_GWAS_significant_variants, AGVs_intersect_count, LD_variants_intersect_count = intersect_GWAS(args.GWAS_variants, AGV_set, LD_variant_set)

	write_header = not os.path.exists(args.output) or os.path.getsize(args.output) == 0

	with open(args.output, 'a') as out:
		if write_header:
			out.write("Trait\tN_GWAS_significant_variants\tN_AGV_GWAS_significant_variants\tN_AGV_and_LD_variant_GWAS_significant_variants\n")
		out.write(f"{args.GWAS_trait}\t{N_GWAS_significant_variants}\t{AGVs_intersect_count}\t{LD_variants_intersect_count}\n")

def generate_AGV_set():
	AGV_set = set()
	with open(f'/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/AGVs_hg38.bed') as f:
		for line in f:
			fields = line.strip().split('\t')
			chr_ = fields[0]
			pos = fields[2]
			key = f"{chr_}:{pos}"
			AGV_set.add(key)
	return AGV_set

def generate_LD_variant_set():
	AGV_LD_variants_directory = '/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_LD_variants/data/'
	LD_variant_set = set()
	pattern = os.path.join(AGV_LD_variants_directory, 'EUR_chr*_AGV_LD_variants.txt.gz')
	files = glob.glob(pattern)

	for file in files:
		with gzip.open(file, 'rt') as f:
			_ = f.readline()
			for line in f:
				fields = line.strip().split('\t')
				try:
					r2 = float(fields[4])
					if r2 < 0.9:
						continue
					chr_ = fields[0]
					pos = fields[2].split(':')[0]
					key = f"{chr_}:{pos}"
					LD_variant_set.add(key)
				except (IndexError, ValueError):
					continue
	return LD_variant_set

def intersect_GWAS(GWAS_variants_file, AGV_set, LD_variant_set):
	N_GWAS_significant_variants = 0
	AGVs_intersect_count = 0
	LD_variants_intersect_count = 0

	with open(GWAS_variants_file) as f:
		for line in f:
			fields = line.strip().split('\t')
			chr_ = fields[0]
			pos = fields[1]
			key = f"{chr_}:{pos}"

			N_GWAS_significant_variants += 1
			if key in AGV_set:
				AGVs_intersect_count += 1
			if key in LD_variant_set:
				LD_variants_intersect_count += 1
	
	return N_GWAS_significant_variants, AGVs_intersect_count, LD_variants_intersect_count

if __name__ == '__main__':
	main()
