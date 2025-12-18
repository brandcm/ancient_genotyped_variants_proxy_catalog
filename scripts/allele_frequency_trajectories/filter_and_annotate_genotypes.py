# This script filters and adds metadata to an ancestrymap formatted genotype file.
# 06/24/24, Colin M. Brand, University of California San Francisco

import argparse
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--annotation_file', type = str, required = True, help = 'Path to annotation file with sample metadata.')
	parser.add_argument('--genotypes', type = str, required = True, help = 'Path to input genotypes file.')
	parser.add_argument('--output', type = str, required = True, help = 'Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()
	sample_annotation = pd.read_csv(args.annotation_file, sep = '\t', header = 0, low_memory = False, compression='gzip')
	data_source_dict = dict(zip(sample_annotation['Genetic_ID'], sample_annotation['Data_source']))
	date_dict = dict(zip(sample_annotation['Genetic_ID'], sample_annotation['Date_mean']))
	location_dict = dict(zip(sample_annotation['Genetic_ID'], sample_annotation['Location']))
	region_dict = dict(zip(sample_annotation['Genetic_ID'], sample_annotation['Region']))

	genotypes = pd.read_csv(args.genotypes, delim_whitespace = True, names = ['rsID','Sample','GT'])
	genotypes = genotypes[genotypes['GT'] != -1]

	map_annotations_to_genotypes(genotypes, 'Data_source', data_source_dict)
	map_annotations_to_genotypes(genotypes, 'Date_mean', date_dict)
	map_annotations_to_genotypes(genotypes, 'Location', location_dict)
	map_annotations_to_genotypes(genotypes, 'Region', region_dict)

	genotypes = genotypes[~genotypes['Location'].fillna('').str.contains('REF|Neanderthal|Denisova')]
	genotypes = genotypes.groupby('Sample', group_keys=False).apply(prioritize_diploid_shotgun_genotypes)
	genotypes = genotypes.reset_index(drop = True)
	genotypes.to_csv(args.output, sep ='\t', header = True, index = False)

def map_annotations_to_genotypes(df, column, dictionary):
	df[column] = df['Sample'].map(dictionary)

def prioritize_diploid_shotgun_genotypes(df):
	if 'Shotgun.diploid' in df['Data_source'].values:
		return df[df['Data_source'] == 'Shotgun.diploid'].head(1)
	else:
		return df.head(1)

if __name__ == '__main__':
	main()
