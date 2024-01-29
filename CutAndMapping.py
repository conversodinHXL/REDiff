desc="""Identify RNA editing sites from RNAseq and DNAseq alignements (.bam).
Alternatively, reference genome can be used instead of DNAseq,
but at the cost of higher false positive. 

TBD:
- editing from heterozygous sites?
"""
epilog="""Author:
15216716554@163.com

beijing/China 28/07/2017
"""
import os,sys,re
from datetime import datetime


#python GATK2_1.py -r /data/ucsc.hg19.fasta -i /data/SRP026084/SRR901895_1.fastq.gz  /data/SRP026084/SRR901895_2.fastq.gz -T /data/EDITINGSoftware/ -t 2 -o test19

def checkSoftware():
	if(os.system("hisat2 --version") == "-bash: hisat2: command not found"):
		print("no hisat2, please install")
	if(os.system("samtools") == "-bash: samtools: command not found"):
		print("no samtools, please install")
	if(re.match("not found",os.system("REDItoolKnown.py"))):
		print("no REDItoolKnown.py, please download from github and remove to /usr/bin/")

def mapping(input,refrence,refIndex,output,threads):
	hisat='hisat2 -p '+str(threads)+' -x '+refIndex
	if len(input)==1:
		hisat=hisat+' '+input[0]
	if len(input)==2:
		hisat=hisat+' -1 '+input[0]+" "+'-2 '+input[1]
	hisat=hisat+' -S '+output+'/'+output+'.sam 2> '+output+'/'+output+'.mapping.log'
	print hisat
	os.system(hisat)

def samtools(threads,output):
	samtools='samtools '
	samtoolsSort=samtools+' sort --threads '+str(threads)+'  -o '+output+'/sort.bam '+output+'/'+output+'.sam'
	samtoolsIndex=samtools+' index '+output+'/sort.bam'
	removesam='rm '+output+'/'+output+'.sam'
	print samtoolsSort
	print samtoolsIndex
	os.system(samtoolsSort)
	os.system(samtoolsIndex)
	os.system(removesam)

def REDItools(refrence,REDIportal,minAltReads,minDepth,threads,output):
	REDK='REDItoolKnown.py '
	REDK=REDK+' -i '+output+'/sort.bam -f '+refrence+' -l '+REDIportal+' -t '+str(threads)+' -c '+str(minDepth)+' -T 6-0  -p -e -d -u -m20  -v '+str(minAltReads)+' -n 0.0 -o '+output+'/'+output
	print REDK
	CP='cp '+output+'/'+output+'known_*/out* '+output+'.xls'
	print CP
	os.system(REDK)
	os.system(CP)

def AnnotateSNV(toolbox):
	if not os.path.isfile('mpileup.avinput'):
			sys.stderr.write("No such file: mpileup.avinput\n")
			sys.exit(1)
	Annovar=toolbox+'/annovar/table_annovar.pl '
	Annovar=Annovar+' mpileup.avinput '+toolbox+'/annovar/humandb/ -buildver hg19  -out AnnotateSNV -protocol Alu,snp138,refGene,RBP_all,cytoBand,dgvMerged,esp6500siv2_all,exac03,genomicSuperDups,gerp++elem,targetScanS,wgRna,phastConsElements100way,phastConsElements46way,rmsk -operation r,f,g,r,r,r,f,f,r,f,r,r,r,r,r   -nastring . -csvout -thread 2 -remove'
	os.system(Annovar)


def processAll(file):
	mapping(file)
	samtools(file)
	transformRes(file)

def main():
	import argparse
	usage  = "%(prog)s [options]" 
	parser  = argparse.ArgumentParser(usage=usage, description=desc, epilog=epilog, \
                                      formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose")
	parser.add_argument('--version', action='version', version='0.99a')
	parser.add_argument('-o','--output',required=False,  help="where results put")
	parser.add_argument('-i','--input',nargs='*',default=[],required=False,  help="input RNA-seq fastq file")
	parser.add_argument('-r','--refrence',required=False,  help="refrence genome fasta,only for hg19")
	parser.add_argument('-ri','--refrenceIndex',required=False,  help="STAR Index refrence genome fasta,only for hg19")
	parser.add_argument("-k", "--REDIportal",required=False,  help="path to REDIportal databases") 
	parser.add_argument("--minDepth", default=10,  type=int,
                        help="minimal depth of coverage [%(default)s]")
	parser.add_argument("--minAltReads", default=1,  type=int,
                        help="minimum no. of reads with alternative base to call RNA editing [%(default)s]")
	parser.add_argument("--minRNAfreq",  default=0, type=float,
                        help="min frequency for RNA editing base [%(default)s]")
	parser.add_argument("-m", "--mapq", default=15, type=int, help="mapping quality [%(default)s]")
	parser.add_argument("--bcq", default=20, type=int, help="basecall quality [%(default)s]")
	parser.add_argument("-t", "--threads", default=4, type=int, help="number of cores to use [%(default)s]")

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	o = parser.parse_args()
	if o.verbose:
		sys.stderr.write("Options: %s\n"%str(o))
	#checkSoftware()
	fileLists=o.input
	for file in fileLists:
		if not os.path.isfile(file):
			sys.stderr.write("No such file: %s\n"%file)
			sys.exit(1)
	if o.output=="-":
		output = sys.stdout
	elif os.path.exists(o.output) :
		sys.stderr.write("The output file %s exists!\n"%o.output)
	os.system('rm -rf '+o.output)
	os.system('mkdir '+o.output)
	os.system('cd '+o.output)
	mapping(o.input,o.refrence,o.refrenceIndex,o.output,o.threads)
	samtools(o.threads,o.output)
	REDItools(o.refrence,o.REDIportal,o.minAltReads,o.minDepth,o.threads,o.output)


if __name__=='__main__': 
	t0 = datetime.now()
	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("\nCtrl-C pressed!      \n")
	dt = datetime.now()-t0
	sys.stderr.write("#Time elapsed: %s\n" % dt)
