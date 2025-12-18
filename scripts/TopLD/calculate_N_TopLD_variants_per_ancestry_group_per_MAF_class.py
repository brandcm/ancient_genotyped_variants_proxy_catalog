import os
import gzip
from collections import defaultdict

def main():
	TopLD_directory_path = "/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/TopLD/data"
	ancestry_group_counts = count_TopLD_variants_by_ancestry_group(TopLD_directory_path)

	output_file = "/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/TopLD/calculate_N_TopLD_variants_per_ancestry_group_per_MAF_class.txt"
	write_proportions_to_file(ancestry_group_counts, output_file)

def classify_MAF(MAF):
	"""Classify MAF into categories: UR (Ultra Rare), R (Rare), LF (Low Frequency), or C (Common)."""
	if MAF < 0.001:
		return "UR"
	elif MAF < 0.01:
		return "R"
	elif MAF < 0.05:
		return "LF"
	else:
		return "C"

def parse_file(file_path, chr):
	"""Parse a single file and classify variants by MAF."""
	class_counts = defaultdict(int)
	try:
		with gzip.open(file_path, 'rt') as file:
			next(file)
			for line in file:
				fields = line.strip().split(',')
				try:
					MAF = float(fields[2])  # Assuming MAF is in the 5th column (index 4)
					class_type = classify_MAF(MAF)
					class_counts[class_type] += 1
				except ValueError:
					print(f"Warning: Invalid MAF value in file '{file_path}': {fields[4]}")
	except Exception as e:
		print(f"Error reading file '{file_path}': {e}")
	return class_counts

def count_TopLD_variants_by_ancestry_group(TopLD_directory_path):
	"""
	Parses TopLD variant annotation files and counts the number of variants per MAF class for each ancestry group.

	Args:
		TopLD_directory_path (str): Path to the directory containing files.

	Returns:
		dict: A nested dictionary where keys are ancestry group and values are dictionaries of MAF class counts.
	"""
	if not os.path.isdir(TopLD_directory_path):
		print(f"Error: Directory '{TopLD_directory_path}' does not exist.")
		return {}

	ancestry_groups = ['AFR', 'EAS', 'EUR', 'SAS']
	chromosomes = [str(i) for i in range(1, 23)] + ['X']

	# Build a set of all files in the directory for fast lookup
	existing_files = set(os.listdir(TopLD_directory_path))
	ancestry_group_counts = {ancestry_groups: defaultdict(int) for ancestry_group in ancestry_groups}

	for chr in chromosomes:
		for ancestry_group in ancestry_groups:
			filename = f"{ancestry_group}_chr{chr}_no_filter_0.2_1000000_info_annotation.csv.gz"
			file_path = os.path.join(TopLD_directory_path, filename)

			if filename in existing_files:
				class_counts = parse_file(file_path, chr)
				for class_type, count in class_counts.items():
					ancestry_group_counts[ancestry_group][class_type] += count
			else:
				print(f"Warning: File '{file_path}' does not exist. Skipping.")

	return ancestry_group_counts

def write_proportions_to_file(ancestry_group_counts, output_file):
	"""Write the MAF class proportions to a text file."""
	with open(output_file, 'w') as file:
		file.write("ancestry_group\tMAF_class\tproportion\n")
		for ancestry_group, counts in ancestry_group_counts.items():
			total_variants = sum(counts.values())
			for class_type, count in counts.items():
				proportion = count / total_variants if total_variants > 0 else 0
				file.write(f"{ancestry_group}\t{class_type}\t{proportion:.6f}\n")

if __name__ == '__main__':
	main()