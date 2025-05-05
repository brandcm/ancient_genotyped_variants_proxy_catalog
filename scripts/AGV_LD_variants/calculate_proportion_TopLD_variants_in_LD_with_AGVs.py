import argparse
import os
import numpy as np
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ancestry_group', type=str, required=True, help='Ancestry group ID to analyze (AFR, EAS, EUR, or SAS).')
	parser.add_argument('--out', type=str, required=True, help='Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	pd.options.display.max_columns = 100

	TopLD_directory_path = "/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/TopLD/data"
	LD_directory_path = "/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_LD_variants/data"
	ancestry_group = args.ancestry_group
	MAF_classes = ["UR", "R", "LF", "C"]
	LD_thresholds = [0.2, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1]

	MAF_class_sums = sum_TopLD_variants_per_MAF_class(TopLD_directory_path, ancestry_group)
	if not MAF_class_sums:
		print("Error: Could not calculate MAF class counts.")
		return

	proportions_df = count_TopLD_variants_per_LD_threshold_and_MAF_class(ancestry_group, TopLD_directory_path, LD_directory_path, MAF_classes, MAF_class_sums, LD_thresholds)
	proportions_df.to_csv(args.out, sep='\t', header=True, index=False)

def sum_TopLD_variants_per_MAF_class(TopLD_directory_path, ancestry_group):
	"""
	Parses TopLD variant annotation files and sums the number of variants per MAF class for a given ancestry_group.

	Args:
		directory_path (str): Path to the directory containing files.
		ancestry_group (str): ancestry_group ID to analyze (AFR, EAS, EUR, or SAS).

	Returns:
		list: Sum for each MAF class (MAF_class_sums).
	"""
	# Initialize sums
	MAF_class_sums = [0, 0, 0, 0]  # 0-0.001, 0.001-0.01, 0.01-0.05, 0.05+

	# Check directory exists
	if not os.path.isdir(TopLD_directory_path):
		print(f"Error: Directory '{TopLD_directory_path}' does not exist.")
		return

	# Define filenames
	chrs = [str(i) for i in range(1, 23)] + ['X']
	filenames = [f"{ancestry_group}_chr{chr}_no_filter_0.2_1000000_info_annotation.csv.gz" for chr in chrs]

	# Process each file in the directory
	for filename in filenames:
		file_path = os.path.join(TopLD_directory_path, filename)

		if os.path.isfile(file_path):
			print(f"Processing file: {filename}")

			try:
				MAFs = np.genfromtxt(file_path, delimiter=',', skip_header=1, usecols=2, invalid_raise=False)

				MAF_class_counts = [
					np.sum((MAFs >= 0) & (MAFs < 0.001)),
					np.sum((MAFs >= 0.001) & (MAFs < 0.01)),
					np.sum((MAFs >= 0.01) & (MAFs < 0.05)),
					np.sum(MAFs >= 0.05)
				]

				MAF_class_sums = [MAF_class_sums[i] + MAF_class_counts[i] for i in range(4)]
			except Exception as e:
				print(f"Error processing file '{filename}': {e}")

	return MAF_class_sums

def count_TopLD_variants_per_LD_threshold_and_MAF_class(ancestry_group, TopLD_directory_path, LD_directory_path, MAF_classes, MAF_class_sums, LD_thresholds):
	"""
	Calcalates the number of variants in LD with at least one AGV at various LD thresholds for each MAF class.

	Args:
		directory_path (str): Path to directory containing LD files.
		ancestry_group (str): ancestry_group ID to analyze (AFR, EAS, EUR, or SAS).
		LD_thresholds (list): List of LD thresholds for which to calculate proportions.
		MAF_classes (list): List of MAF classes.
		MAF_class_sums (list): Total number of variants for each MAF class across all chromosomes.
		LD_thresholds (list): List of r-squared LD thresholds for which to calculate counts.
	
	Returns:
		pd.Dataframe: DataFrame containing number of variants in LD with at least one AGV at various LD thresholds for each MAF class.
	"""

	# Initialize dictionary
	counts_dict = {MAF_class: [0] * len(LD_thresholds) for MAF_class in MAF_classes}

	def classify_MAF(MAF):
		if MAF < 0.001:
			return "UR"
		elif MAF < 0.01:
			return "R"
		elif MAF < 0.05:
			return "LF"
		else:
			return "C"

	chrs = [str(i) for i in range(1, 23)] + ['X']
	for chr in chrs:
		annotation_file_path = os.path.join(TopLD_directory_path, f"{ancestry_group}_chr{chr}_no_filter_0.2_1000000_info_annotation.csv.gz")
		LD_file_path = os.path.join(LD_directory_path, f"{ancestry_group}_chr{chr}_AGV_LD_variants.txt.gz")

		if os.path.isfile(annotation_file_path) and os.path.isfile(LD_file_path):
			annotation_df = pd.read_csv(annotation_file_path, compression='gzip', sep=',', header=0)
			annotation_df = annotation_df.rename(columns={'Uniq_ID': 'LDV'})
			annotation_df['MAF_class'] = annotation_df['MAF'].apply(classify_MAF)

			AGV_LDV_df = pd.read_csv(LD_file_path, compression='gzip', sep='\t', header=None, names=['chr','AGV','LDV','rsID','R2','D','corr'])
			AGV_LDV_df = AGV_LDV_df.merge(annotation_df[['LDV','MAF','MAF_class']], on='LDV', how='left')

			for MAF_class in MAF_classes:
				MAF_class_df = AGV_LDV_df[AGV_LDV_df['MAF_class'] == MAF_class]

				for i, LD_threshold in enumerate(LD_thresholds):
					N_variants_at_LD_threshold = MAF_class_df[MAF_class_df['R2'] >= LD_threshold]['LDV'].nunique()
					counts_dict[MAF_class][i] += N_variants_at_LD_threshold

	counts_list = []
	for MAF_class, counts in counts_dict.items():
		row = [MAF_class] + counts + [MAF_class_sums[MAF_classes.index(MAF_class)]]
		counts_list.append(row)

	counts_header = ['MAF_class'] + [f'R2_{threshold}' for threshold in LD_thresholds] + ['Sum']
	counts_df = pd.DataFrame(counts_list, columns=counts_header)
	return counts_df

if __name__ == '__main__':
	main()