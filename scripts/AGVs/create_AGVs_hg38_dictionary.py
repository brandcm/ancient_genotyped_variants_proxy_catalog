import pickle

chrs_dict = {}

with open('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/AGVs_hg38.bed', 'r') as input_file:
	for line in input_file:
		fields = line.strip().split()
		chromosome = fields[0]
		chrs_dict.setdefault(chromosome, []).append(':'.join([fields[2], fields[3], fields[4]]))

with open('/wynton/group/capra/projects/ancient_genotyped_variants_proxy_catalog/data/AGVs/AGVs_hg38.pkl', 'wb') as out:
	pickle.dump(chrs_dict, out)
