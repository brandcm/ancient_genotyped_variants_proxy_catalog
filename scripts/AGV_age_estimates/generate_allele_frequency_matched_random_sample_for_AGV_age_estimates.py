import os
import pandas as pd
seed = 106

def main():
	variants = pd.read_csv('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_age_estimates/high_quality_AGV_age_estimates_single_estimate_per_variant_non_missing_AF.txt.gz', sep = '\t', header = 0, compression = 'gzip')
	variants['gnomAD_AF_bin'] = pd.cut(variants['gnomAD_AF'], bins = [i/100 for i in range(0, 101)])
	variants['gnomAD_AF_bin'] = variants['gnomAD_AF_bin'].astype(str)

	combined_estimates = variants[variants['DataSource'] == 'Combined']
	SGDP_estimates = variants[variants['DataSource'] == 'SGDP']
	TGP_estimates = variants[variants['DataSource'] == 'TGP']

	combined_bin_sizes = create_AF_bin_dictionary(combined_estimates)
	SGDP_bin_sizes = create_AF_bin_dictionary(SGDP_estimates)
	TGP_bin_sizes = create_AF_bin_dictionary(TGP_estimates)

	combined_dict = dict(zip(combined_bin_sizes['gnomAD_AF_bin'], combined_bin_sizes['N']))
	SGDP_dict = dict(zip(SGDP_bin_sizes['gnomAD_AF_bin'], SGDP_bin_sizes['N']))
	TGP_dict = dict(zip(TGP_bin_sizes['gnomAD_AF_bin'], TGP_bin_sizes['N']))

	quality_HGD_variants_ages_frequencies = retrieve_quality_HGD_variants_with_AFs()
	quality_HGD_variants_ages_frequencies['gnomAD_AF_bin'] = pd.cut(quality_HGD_variants_ages_frequencies['gnomAD_AF'], bins = [i/100 for i in range(0, 101)])
	quality_HGD_variants_ages_frequencies['gnomAD_AF_bin'] = quality_HGD_variants_ages_frequencies['gnomAD_AF_bin'].astype(str)
	quality_HGD_variants_ages_frequencies['DataSource'] = quality_HGD_variants_ages_frequencies['DataSource'].str.replace(r'\s', '', regex=True)

	combined_random_variants = generate_allele_frequency_matched_sample(quality_HGD_variants_ages_frequencies, 'Combined', combined_dict, seed)
	SGDP_random_variants = generate_allele_frequency_matched_sample(quality_HGD_variants_ages_frequencies, 'SGDP', SGDP_dict, seed)
	TGP_random_variants = generate_allele_frequency_matched_sample(quality_HGD_variants_ages_frequencies, 'TGP', TGP_dict, seed)
	random_variants = pd.concat([combined_random_variants,SGDP_random_variants,TGP_random_variants])
	random_variants.to_csv('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_age_estimates/allele_frequency_matched_random_sample_for_AGV_age_estimates.txt.gz', sep = '\t', header = True, index = False, compression = 'gzip')

def create_AF_bin_dictionary(df):
	AF_bin_sizes = df.groupby(by = ['gnomAD_AF_bin']).size().to_frame('N').reset_index()
	AF_bin_sizes['gnomAD_AF_bin'] = AF_bin_sizes['gnomAD_AF_bin'].astype(str)
	return AF_bin_sizes

def retrieve_quality_HGD_variants_with_AFs():
	merged_variants = []
	chromosomes = [str(i) for i in range(1, 23)]
	HGD_directory_path = '/wynton/group/capra/data/human_genome_dating/2024-01-02/'

	for chr in chromosomes:
		HGD_file = f'atlas.chr{chr}.csv.gz'
		HGD_file_path = os.path.join(HGD_directory_path, HGD_file)

		if not os.path.exists(HGD_file_path):
			print(f"Warning: Missing HGD file for chromosome {chr}")
			continue

		HGD_df = pd.read_csv(HGD_file_path, compression='gzip', sep=',', skiprows=4, names=['VariantID','Chromosome','Position','AlleleRef','AlleleAlt','AlleleAnc','DataSource','NumConcordant','NumDiscordant','AgeMode_Mut','AgeMean_Mut','AgeMedian_Mut','AgeCI95Lower_Mut','AgeCI95Upper_Mut','QualScore_Mut','AgeMode_Rec','AgeMean_Rec','AgeMedian_Rec','AgeCI95Lower_Rec','AgeCI95Upper_Rec','QualScore_Rec','AgeMode_Jnt','AgeMean_Jnt','AgeMedian_Jnt','AgeCI95Lower_Jnt','AgeCI95Upper_Jnt','QualScore_Jnt'])
		HGD_df['AlleleRef'] = HGD_df['AlleleRef'].str.replace(r'\s', '', regex=True)
		HGD_df['AlleleAlt'] = HGD_df['AlleleAlt'].str.replace(r'\s', '', regex=True)
		HGD_df = HGD_df[['Chromosome','Position','AlleleRef','AlleleAlt','DataSource','AgeMode_Jnt','QualScore_Jnt']]
		HGD_df = HGD_df[HGD_df['QualScore_Jnt'] >= 0.5]

		gnomAD_AFs_directory = '/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGV_age_estimates/gnomAD_AFs/'
		gnomAD_AFs_file = f'chr{chr}_HGD_gnomAD_AFs.txt'
		gnomAD_file_path = os.path.join(gnomAD_AFs_directory, gnomAD_AFs_file)

		if not os.path.exists(gnomAD_file_path):
			print(f"Warning: Missing gnomAD file for chromosome {chr}")
			continue

		gnomAD_df = pd.read_csv(gnomAD_file_path, names=['Chromosome','Position','AlleleRef','AlleleAlt','gnomAD_AF'], sep='\t')
		merged_df = pd.merge(HGD_df, gnomAD_df, how='inner', on=['Chromosome','Position','AlleleRef','AlleleAlt'])
		merged_variants.append(merged_df)

	return pd.concat(merged_variants, ignore_index=True) if merged_variants else pd.DataFrame()

def generate_allele_frequency_matched_sample(dataframe, data_source, dictionary, seed):
	df = dataframe[dataframe['DataSource'] == data_source]
	random_matched_variants = []
	for key, value in dictionary.items():
		matched_frequency_variants = df[df['gnomAD_AF_bin'] == key]
		random_sampled_variants = matched_frequency_variants.sample(n=value, random_state=seed)
		random_matched_variants.append(random_sampled_variants)
	random_matched_variants_df = pd.concat(random_matched_variants)
	return random_matched_variants_df[['DataSource','AgeMode_Jnt','gnomAD_AF']]

if __name__ == '__main__':
	main()
