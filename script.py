import pandas as pd
import pysam
import logging
import click
import glob

def get_indent(fai):
	f = open(fai, 'r')
	line = f.readline().split('\t')
	f.close()
	return int(line[2])

def get_nucleo(cur, fa, indent):
	fa.seek(cur + indent) 
	return fa.read(1)
	


@click.command()
@click.option('--ifile', type=str, help='Input file with two alleles and adresses')
@click.option('--ofile', type=str, help='Name of utput file with identified reference allele')

def run(ifile, ofile):
	"""Try identify in input file reference allele with information from chrs fasta files"""
	FORMAT = '%(asctime)s %(message)s'
	logging.basicConfig(format=FORMAT, filename='log.txt',
     level=logging.INFO, filemode="w")
	df = pd.read_csv(ifile, sep='\t')
	try:
		df = pd.read_csv(ifile, sep='\t')
	except Exception as e:
		logging.warn(str(e))

	logging.info("Get alleles file.")
	df['GB38_position'].astype(int)
	chrs = ['chr' + str(i) for i in range(1,23)]
	logging.info("Get fasta files.")
	print(chrs)
	chr_path = 'chrs/'
	for chr in chrs:
		try:
			fasta = pysam.Fastafile(chr_path + chr)
		except:
			logging.warn(chr + 'is not fasta or not find!')
			break

	chroms_num = [i for i in range(1,23)]
	chr_dict = dict(zip(chroms_num,chrs))
	chr_dfs = []
	for chr in chr_dict.keys():
		indent = get_indent(chr_path + chr_dict[chr] + '.fai')
		fa_file = open(chr_path + chr_dict[chr], 'r')
		chr_df = df[df['chromosome']==chr]
		chr_df['nucleo_from_fa'] = df['GB38_position'].apply(lambda x: get_nucleo(x, fa_file, indent))
		chr_dfs.append(chr_df)
		logging.info(f"Get nucleo from {chr_dict[chr]}.")
		fa_file.close()
		
	ref_df = pd.concat(chr_dfs)
	a1 = ref_df[ref_df['nucleo_from_fa']==ref_df['allele1']].shape[0]
	logging.info(f"Get with nucleo coincidense allele1 {a1}.")
	a2 = ref_df[ref_df['nucleo_from_fa']==ref_df['allele2']].shape[0]
	logging.info(f"Get with nucleo coincidense allele2 {a2}.")
	cols = ['#CHROM', 'POS', 'ID', 'REF', 'ALT']
	if a1 > a2:
		ref_df = ref_df.rename(columns = {'allele1':'REF', 'allele2':'ALT', 'chromosome':'#CHROM', 'rs#':'ID', 'GB38_position':'POS'})
		logging.info(f"Allele1 win!!!!!!!!!!")
	else:
		ref_df = ref_df.rename(columns = {'allele2':'REF', 'allele1':'ALT', 'chromosome':'#CHROM', 'rs#':'ID', 'GB38_position':'POS'})
		logging.info(f"Allele2 win!!!!!!!!!!")
	ref_df = ref_df[cols]
	ref_df.to_csv(ofile, sep='\t')

if __name__=='__main__':
	run()





