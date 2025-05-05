import os
import gzip

def main():
	TopLD_directory_path = "/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/TopLD/data"
	unique_variant_count = count_unique_TopLD_variants(TopLD_directory_path)
	print(f"Total unique variants: {unique_variant_count}")

def parse_file(file_path, chr):
	"""Parse a single file and returns the set of unique variants."""
	unique_variants = set()
	try:
		with gzip.open(file_path, 'rt') as file:
			next(file)
			for line in file:
				fields = line.strip().split(',')
				variant = chr + '_' + fields[5]
				unique_variants.add(variant)
	except Exception as e:
		print(f"Error reading file '{file_path}': {e}")
	return unique_variants

def count_unique_TopLD_variants(TopLD_directory_path):
	"""
	Parses TopLD variant annotation files and counts the total number of unique variants.

	Args:
		TopLD_directory_path (str): Path to the directory containing files.

	Returns:
		int: Sum of unique TopLD variants across all ancestry groups and chromosomes.
	"""
	if not os.path.isdir(TopLD_directory_path):
		print(f"Error: Directory '{TopLD_directory_path}' does not exist.")
		return 0

	ancestry_groups = ['AFR', 'EAS', 'EUR', 'SAS']
	chromosomes = [str(i) for i in range(1, 23)] + ['X']

	# Build a set of all files in the directory for fast lookup
	existing_files = set(os.listdir(TopLD_directory_path))
	total_unique_variants = set()

	for chr in chromosomes:
		for ancestry_group in ancestry_group:
			filename = f"{ancestry_group}_chr{chr}_no_filter_0.2_1000000_info_annotation.csv.gz"
			file_path = os.path.join(TopLD_directory_path, filename)

			if filename in existing_files:
				file_variants = parse_file(file_path, chr)
				total_unique_variants.update(file_variants)
			else:
				print(f"Warning: File '{file_path}' does not exist. Skipping.")

	return len(total_unique_variants)

if __name__ == '__main__':
	main()