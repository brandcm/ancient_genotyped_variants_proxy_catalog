import argparse
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--HGD_file', type=str, required=True, help='Path to HGD file.')
	parser.add_argument('--gnomAD_AFs_file', type=str, required=True, help='Path to file with gnomAD allele frequencies. Formatted as a tab-delimited file with chr, pos, ref, alt, and AF.')
	parser.add_argument('--output', type=str, required=True, help='Path to output file.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()
	map_allele_frequencies(args.HGD_file, args.gnomAD_AFs_file, args.output)

def map_allele_frequencies(HGD_file, gnomAD_AFs_file, output):
	HGD_df = pd.read_csv(HGD_file, sep = '\t', names = ['VariantID','Chromosome','Position','AlleleRef','AlleleAlt','AlleleAnc','DataSource','NumConcordant','NumDiscordant','AgeMode_Mut','AgeMean_Mut','AgeMedian_Mut','AgeCI95Lower_Mut','AgeCI95Upper_Mut','QualScore_Mut','AgeMode_Rec','AgeMean_Rec','AgeMedian_Rec','AgeCI95Lower_Rec','AgeCI95Upper_Rec','QualScore_Rec','AgeMode_Jnt','AgeMean_Jnt','AgeMedian_Jnt','AgeCI95Lower_Jnt','AgeCI95Upper_Jnt','QualScore_Jnt'])
	AFs_df = pd.read_csv(gnomAD_AFs_file, sep = '\t', header = None, names = ['Chromosome','Position','AlleleRef','AlleleAlt', 'gnomAD_AF'])
	merged_df = pd.merge(HGD_df, AFs_df, how='left', on=['Chromosome','Position','AlleleRef','AlleleAlt'])

	merged_df.to_csv(output, sep = '\t', index = False)

if __name__ == '__main__':
	main()