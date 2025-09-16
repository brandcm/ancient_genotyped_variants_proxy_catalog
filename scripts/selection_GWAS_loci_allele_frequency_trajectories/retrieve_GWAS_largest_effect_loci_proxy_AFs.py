import argparse
import gzip
import numpy as np
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--rsIDs_file', type = str, required = True, help = 'Path to rsIDs file formatted as a tab-delimited file where chr and rsID are the fields.')
	parser.add_argument('--chr', type = str, required = True, help = 'Chromosome to analyze.')
	parser.add_argument('--VCF', type = str, required = True, help = 'Path to VCF file.')
	parser.add_argument('--output', type = str, required = True, help = 'Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	print("=== DEBUG INFO ===")
	print(f"rsIDs file: {args.rsIDs_file}")
	print(f"Chromosome: {args.chr}")
	print(f"VCF file:   {args.VCF}")
	print(f"Output:     {args.output}")
	print("==================")

	rsIDs = args.rsIDs_file
	chr_ = args.chr
	VCF_path = args.VCF
	output_path = args.output

	max_samples = 9990
	bin_size = 1000
	max_years = 10000

	calculate_AF_per_bin(
		VCF_path=VCF_path,
		rsIDs_path=rsIDs,
		annotation_path='/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/allele_frequency_trajectories/AADR_sample_annotation_basic.txt.gz',  # hardcoded or could make an argument
		output_path=output_path,
		chromosome=chr_,
		max_samples=max_samples,
		bin_size=bin_size,
		max_years=max_years
	)

def calculate_AF_per_bin(VCF_path, rsIDs_path, annotation_path, output_path, chromosome='chr2', max_samples=9990, bin_size=1000, max_years=10000):
	"""
	Parse VCF, filter for variants on a given chromosome, map samples to metadata,
	and calculate allele frequencies per 1000-year bin (last 10,000 years) for Europe samples.
	"""
	# -------------------------
	# Load rsID -> chr mapping
	# -------------------------
	rsids_df = pd.read_csv(rsIDs_path, sep='\t', header=0)  # full header expected
	rsids_df = rsids_df[rsids_df['AGV_rsID'].notna() & (rsids_df['AGV_rsID'] != '')]
	rsid_to_beta = rsids_df.groupby('AGV_rsID')['GWAS_beta'].apply(list).to_dict()
	rsid_to_effect = rsids_df.set_index('AGV_rsID')['effect_allele'].to_dict()
	chr_variants = set(rsids_df.loc[rsids_df['chr'] == chromosome, 'AGV_rsID'])

	# -------------------------
	# Load annotation data
	# -------------------------
	annotation_df = pd.read_csv(annotation_path, sep='\t', compression='gzip')
	# Only keep Europe samples and within last max_years
	annotation_df = annotation_df[(annotation_df['Region']=='Europe') & (annotation_df['Date_mean'] <= max_years)]
	# Create 1000-year bins
	bins = np.arange(0, max_years+bin_size, bin_size)
	bin_labels = [f"{b}-{b+bin_size-1}" for b in bins[:-1]]
	annotation_df['time_bin'] = pd.cut(annotation_df['Date_mean'], bins=bins, labels=bin_labels, include_lowest=True)
	sample_to_bin = dict(zip(annotation_df['Genetic_ID'], annotation_df['time_bin']))

	# -------------------------
	# Open VCF and output file
	# -------------------------
	open_in = gzip.open if VCF_path.endswith('.gz') else open
	with open_in(VCF_path, 'rt') as VCF, open(output_path, 'w') as out:
		# Write header
		out.write('rsID\tGWAS_beta\t' + '\t'.join(bin_labels) + '\n')

		for line in VCF:
			if line.startswith('##'):
				continue
			elif line.startswith('#CHROM'):
				sample_names = line.strip().split('\t')[9:9+max_samples]
				# Only keep samples present in metadata
				valid_indices = [i for i, s in enumerate(sample_names) if s in sample_to_bin]
				sample_names = [sample_names[i] for i in valid_indices]
				continue

			fields = line.strip().split('\t')
			rsID = fields[2]
			if rsID not in chr_variants:
				continue  # skip variants not on target chromosome

			ancient_samples = fields[9:9+max_samples]
			# Filter to valid samples
			ancient_samples = [ancient_samples[i] for i in valid_indices]

			# Build dataframe: sample -> alt allele count, bin
			alt_counts = []
			bins_per_sample = []
			for sample_name, geno_field in zip(sample_names, ancient_samples):
				if not is_non_missing(geno_field):
					continue
				gt = geno_field.split(':')[0]
				# Sum of alt alleles
				if '|' in gt:
					alleles = gt.split('|')
				else:
					alleles = gt.split('/')
				alt_count = sum(int(a) for a in alleles)
				alt_counts.append(alt_count)
				bins_per_sample.append(sample_to_bin[sample_name])

			if len(alt_counts) == 0:
				# No valid samples
				af_row = ['NaN']*len(bin_labels)
			else:
				df_var = pd.DataFrame({'alt_count': alt_counts, 'time_bin': bins_per_sample})
				# Sum alt alleles and total alleles per bin
				freq_per_bin = df_var.groupby('time_bin')['alt_count'].agg(['sum','count'])
				freq_per_bin['af'] = freq_per_bin['sum'] / (2*freq_per_bin['count'])
				# Fill missing bins with NaN
				af_row = [freq_per_bin['af'].get(b, np.nan) for b in bin_labels]

			effect_allele = rsid_to_effect.get(rsID, None)
			if effect_allele is not None:
				ref_allele = fields[3]
				alt_allele = fields[4]
				if effect_allele == ref_allele:
					af_row = [1 - x if x is not np.nan else np.nan for x in af_row]

			# Write line
			for beta in rsid_to_beta.get(rsID, [np.nan]):
				out.write(f"{rsID}\t{beta}\t" + '\t'.join(str(x) for x in af_row) + '\n')

	print(f"Allele frequencies per bin saved to {output_path}")

def is_non_missing(genotype_field):
	"""Return True if genotype is called (not missing)."""
	return genotype_field.split(':')[0] not in {'./.', '.|.'}

if __name__ == "__main__":
	main()