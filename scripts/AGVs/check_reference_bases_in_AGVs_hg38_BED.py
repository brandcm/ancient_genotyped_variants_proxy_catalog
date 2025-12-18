import argparse
import gzip
import pysam

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--fasta', type = str, required = True, help = 'Path to input FASTA file')
	parser.add_argument('--bed', type = str, required = True, help = 'Path to input BED file.')
	parser.add_argument('--output', type = str, required = True, help = 'Path to output file. Will overwrite if it exists.')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	with open(args.bed, 'r') as bed, pysam.FastaFile(args.fasta) as fasta, open(args.output, 'w') as out:
		for line in bed:
			fields = line.strip().split()
			chr = fields[0]
			chr = chr[3:]
			start = int(fields[1])
			end = int(fields[2])
			hg19_ref = fields[3]
			hg38_ref = fasta.fetch(chr, start, end).upper()
			alt = fields[4]
			rsID = fields[5]

			if hg19_ref == hg38_ref.upper():
				out.write(f'chr{chr}\t{start}\t{end}\t{hg19_ref}\t{alt}\t{rsID}\n')
			else:
				out.write(f'chr{chr}\t{start}\t{end}\t{hg38_ref}\t{hg19_ref}\t{rsID}\n')
				print(f'Reference base for {rsID} is {hg38_ref} in hg38 not {hg19_ref}.')

if __name__ == '__main__':
	main()
