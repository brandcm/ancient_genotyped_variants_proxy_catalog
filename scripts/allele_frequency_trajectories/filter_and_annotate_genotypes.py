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
	sample_annotation = pd.read_csv(args.annotation_file, sep = '\t', header = 0, low_memory = False)
	data_source_dict = dict(zip(sample_annotation['Genetic ID'], sample_annotation['Data source']))
	date_dict = dict(zip(sample_annotation['Genetic ID'], sample_annotation['Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]']))
	location_dict = dict(zip(sample_annotation['Genetic ID'], sample_annotation['location']))
	region_dict = dict(zip(sample_annotation['Genetic ID'], sample_annotation['region']))

	genotypes = pd.read_csv(args.genotypes, delim_whitespace = True, names = ['rsID','sample','gt'])
	genotypes = genotypes[genotypes['gt'] != -1]

	map_annotations_to_genotypes(genotypes, 'data_source', data_source_dict)
	map_annotations_to_genotypes(genotypes, 'date', date_dict)
	map_annotations_to_genotypes(genotypes, 'location', location_dict)
	map_annotations_to_genotypes(genotypes, 'region', region_dict)

	genotypes = genotypes[~genotypes['location'].fillna('').str.contains('REF|Neanderthal|Denisova')]
	genotypes = genotypes.groupby('sample', group_keys=False).apply(prioritize_diploid_shotgun_genotypes)
	genotypes = genotypes.reset_index(drop = True)
	genotypes.to_csv(args.output, sep ='\t', header = True, index = False)

def map_annotations_to_genotypes(df, column, dictionary):
	df[column] = df['sample'].map(dictionary)

def prioritize_diploid_shotgun_genotypes(df):
	if 'Shotgun.diploid' in df['data_source'].values:
		return df[df['data_source'] == 'Shotgun.diploid'].head(1)
	else:
		return df.head(1)

if __name__ == '__main__':
	main()
