import argparse
import gzip
import pickle

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--dictionary', type=str, required=True, help='Path to variant dictionary.')
	parser.add_argument('--ancestry_group', type=str, required=True, help='Ancestry group from which to identify variants in LD. AFR, EAS, EUR, or SAS.')
	parser.add_argument('--chromosome', type=str, required=True, help='Target chromosome.')
	parser.add_argument('--LD_files_directory', type=str, required=True, help='Path to directory with TopLD files.')
	parser.add_argument('--out_directory', type=str, required=True, help='Path to output directory.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	ancestry_group = args.ancestry_group
	chromosome = args.chromosome
	LD_directory = args.LD_files_directory
	out_directory = args.out_directory

	with open(args.dictionary, 'rb') as dict_file:
		open_dict = pickle.load(dict_file)

	annotation_file_path = f'{LD_directory}{ancestry_group}_{chromosome}_no_filter_0.2_1000000_info_annotation.csv.gz'
	rsID_mapping = load_rsID_mapping(annotation_file_path)

	identify_variants_in_LD(open_dict, chromosome, ancestry_group, LD_directory, out_directory, rsID_mapping)

def load_rsID_mapping(annotation_file_path):
	rsID_mapping = {}
	with gzip.open(annotation_file_path, 'rt') as annotation_file:
		next(annotation_file)
		for variant in annotation_file:
			fields = variant.strip().split(',')
			variant_ID = fields[5]
			rsID = fields[1]
			rsID_mapping[variant_ID] = rsID
	return rsID_mapping

def identify_variants_in_LD(dictionary, chromosome, ancestry_group, LD_directory, out_directory, rsID_mapping):
	if chromosome not in dictionary:
		return

	AGVs = set(dictionary[chromosome])

	ld_file_path = f'{LD_directory}{ancestry_group}_{chromosome}_no_filter_0.2_1000000_LD.csv.gz'
	output_file_path = f'{out_directory}{ancestry_group}_{chromosome}_AGV_LD_variants.txt'

	with gzip.open(ld_file_path, 'rt') as LD_file, open(output_file_path, 'w') as out:
		next(LD_file)
		for line in LD_file:
			fields = line.strip().split(',')
			if fields[2] in AGVs or fields[3] in AGVs:
				AGV = fields[2] if fields[2] in AGVs else fields[3]
				LD_variant = fields[3] if AGV == fields[2] else fields[2]
				LD_variant_rsID = rsID_mapping.get(LD_variant)
				out.write(f'{chromosome}\t{AGV}\t{LD_variant}\t{LD_variant_rsID}\t{fields[4]}\t{fields[5]}\t{fields[6]}\n')

if __name__ == '__main__':
	main()
