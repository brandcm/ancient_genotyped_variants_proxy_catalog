import pandas as pd

def merge_AGV_files(BED_file, AFs_file, TopLD_summary_file, output):
	BED_df = pd.read_csv(BED_file, sep = '\t', names = ['chr','start','pos','ref','alt','rsID'])
	AFs_df = pd.read_csv(AFs_file, sep = '\t', names = ['chr','pos','ref','alt','filter','AF','AFR_AF','EAS_AF','EUR_AF','SAS_AF'])
	merged_df = pd.merge(BED_df[['chr','pos','ref','alt','rsID']], AFs_df, on = ['chr','pos','ref','alt'], how='left')

	TopLD_summary_df = pd.read_csv(TopLD_summary_file, sep = '\t', names = ['ID','TopLD_presence','MAFs','LDV_presence'])
	TopLD_summary_df[['chr', 'pos', 'ref', 'alt']] = TopLD_summary_df['ID'].str.split('_', expand = True)
	TopLD_summary_df['pos'] = TopLD_summary_df['pos'].astype(int)
	TopLD_summary_df.drop(columns = ['ID'], inplace = True)
	final_merged_df = pd.merge(merged_df, TopLD_summary_df, on = ['chr','pos','ref','alt'], how = 'left')

	final_merged_df.to_csv(output, sep = '\t', index = False)

BED_file = '/wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants/1240K_variants_hg38.bed'
AFs_file = '/wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants/AFs.tmp'
TopLD_summary_file = '/wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants/AGVs_TopLD_presence_summary.tmp'
output = '/wynton/group/capra/projects/AADR_proxy_variants/data/1240K_variants/AGVs_hg38_with_gnomAD_AFs.txt'
merge_AGV_files(BED_file, AFs_file, TopLD_summary_file, output)
