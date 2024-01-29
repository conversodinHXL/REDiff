desc="""This script downloads reference files for detecting RNA editing events in human (GRCh37/hg19). The files contain a reference genome indexed for hisat2 (with SNPs marked), RNA editing events from REDIportal, and genome annotations from GENCODE. The total disk space required is 15.5GB. After successful execution, the output directory will contain the following files: 
.:
REDIportals.forREDItools.txt.gz  hg19.ref.fa
TABLE1_hg19.forAnnotation.txt    grch37_snp/       hg19.ref.fa.fai

./grch37_snp:
genome_snp.1.ht2  genome_snp.3.ht2  genome_snp.5.ht2  genome_snp.7.ht2  make_grch37_snp.sh
genome_snp.2.ht2  genome_snp.4.ht2  genome_snp.6.ht2  genome_snp.8.ht2 


example usage: python2.7 prepareRefrence.py -o test_20230711
"""
epilog="""Author: Hu Xiaolin
15216716554@163.com

Shanghai/China 10/10/2023
"""
import os,sys,re
from datetime import datetime

def prepare(output):
	os.system("mkdir "+output)
	os.chdir(output)
	os.system("pwd")
	print("Download reference genome for hisat2")
	os.system("wget https://genome-idx.s3.amazonaws.com/hisat/grch37_snp.tar.gz")
	os.system("tar zxvf  grch37_snp.tar.gz")
	os.system("rm grch37_snp.tar.gz")
	print("Download reference RNA editing events from REDIportal")
	os.system("wget http://srv00.recas.ba.infn.it/webshare/ATLAS/donwload/TABLE1_hg19.txt.gz")
	os.system("gunzip TABLE1_hg19.txt.gz")
	os.system("grep -v 'Region' TABLE1_hg19.txt |awk '{print $1,$2,$5}' | sed 's/ /\t/g' | sed 's/chr//g' | sort -k1,1 -k2,2n  > REDIportals.forREDItools.txt")
	os.system("awk '{if($5==\"-\"){$5=0};if($5==\"+\"){$5=1};print $0}' TABLE1_hg19.txt | sed 's/chr//g' | sed 's/ /\t/g' > TABLE1_hg19.forAnnotation.txt")
	os.system("bgzip REDIportals.forREDItools.txt")
	os.system("rm TABLE1_hg19.txt")
	print("Download reference for hg19")
	os.system("wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_40/GRCh37_mapping/GRCh37.primary_assembly.genome.fa.gz")
	os.system("gunzip GRCh37.primary_assembly.genome.fa.gz")
	os.system("sed 's/chr//g' GRCh37.primary_assembly.genome.fa > hg19.ref.fa")
	os.system("samtools faidx hg19.ref.fa")
	os.system("rm GRCh37.primary_assembly.genome.fa")

def main():
	import argparse
	usage  = "%(prog)s [options]" 
	parser  = argparse.ArgumentParser(usage=usage, description=desc, epilog=epilog, \
                                      formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-o", "--output", default="hg19_ref2", help="path to prepare reference")
	parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose")

	o = parser.parse_args()
	if o.verbose:
		sys.stderr.write("Options: %s\n"%str(o))
	prepare(o.output)

if __name__=='__main__': 
	t0 = datetime.now()
	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("\nCtrl-C pressed!      \n")
	dt = datetime.now()-t0
	sys.stderr.write("#Time elapsed: %s\n" % dt)
