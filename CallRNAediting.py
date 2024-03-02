desc="""This pipeline detects RNA editing events from RNA-seq data. The input is RNA-seq reads in FASTQ format, which can be single- or paired-end. The output is a list of detected RNA editing sites identified by REDItools.
Briefly, the RNA-seq reads are first aligned to the human reference genome (GRCh37/hg19, SNP-masked index from Hisat2) using Hisat2. The alignment files are then converted to BAM, sorted, and indexed using Samtools. Finally, REDItools is used to call known RNA editing events from the REDIPortal database based on the mapped RNA-seq data.
In summary, this pipeline aligns RNA-seq reads, processes the alignments, and then detects RNA editing sites by comparing to known sites from REDIPortal. The key tools utilized are Hisat2, Samtools, and REDItools.

The reference files required for this pipeline can be downloaded using the prepareReference.py script. This script acquires the necessary reference genome, gene annotations, and known RNA editing site databases to provide the reference data needed for read alignment and RNA editing detection. 

The sample results of REDIKnowns is as below:

Region  Position        Reference       Strand  Coverage-q25    MeanQ   BaseCount[A,C,G,T]      AllSubs Frequency       gCoverage-q25   gMeanQ  gBaseCount[A,C,G,T]  gAllSubs        gFrequency
chr21   47739131        A       0       20      34.60   [18, 0, 2, 0]   AG      0.10    30      30.40   [30, 0, 0, 0]   -       0.00
chr21   47739578        A       0       14      38.50   [11, 0, 3, 0]   AG      0.21    26      30.27   [26, 0, 0, 0]   -       0.00
chr21   47739644        A       0       18      36.61   [13, 0, 5, 0]   AG      0.28    23      30.22   [23, 0, 0, 0]   -       0.00
chr21   47739647        A       0       16      36.12   [7, 0, 9, 0]    AG      0.56    18      30.67   [18, 0, 0, 0]   -       0.00

example usage: 
python2.7 CutAndMapping.py -o  K562_ADAR_2 -R ../ouir/ -i  ENCFF093ZYA.fastq ENCFF085DKT.fastq  -ri ../ouir/hg19_ref/grch37_snp/genome_snp -r ../ouir/hg19_ref/GRCh37.primary_assembly.genome.fa -k ../ouir/hg19_ref/REDIportals.forREDItools.txt.gz -t 64

"""
epilog="""Author: Hu Xiaolin
15216716554@163.com

Shanghai/China 10/10/2023
"""
import os,sys,re
from datetime import datetime



def checkSoftware():
	if(os.system("hisat2 --version") == "-bash: hisat2: command not found"):
		print("no hisat2, please install")
	if(os.system("samtools") == "-bash: samtools: command not found"):
		print("no samtools, please install")
	if(re.match("not found",os.system("REDItoolKnown.py"))):
		print("no REDItoolKnown.py, please download from our github and remove to /usr/bin/")

def mapping(input,refrence,refIndex,output,threads):
	hisat='hisat2 -p '+str(threads)+' -x '+refIndex
	if len(input)==1:
		hisat=hisat+' '+input[0]
	if len(input)==2:
		hisat=hisat+' -1 '+input[0]+" "+'-2 '+input[1]
	hisat=hisat+' -S '+output+'/'+output+'.sam 2> '+output+'/'+output+'.mapping.log'
	print(hisat)
	os.system(hisat)

def samtools(threads,output):
	samtools='samtools '
	samtoolsSort=samtools+' sort --threads '+str(threads)+'  -o '+output+'/sort.bam '+output+'/'+output+'.sam'
	samtoolsIndex=samtools+' index '+output+'/sort.bam'
	removesam='rm '+output+'/'+output+'.sam'
	print(samtoolsSort)
	print(samtoolsIndex)
	os.system(samtoolsSort)
	os.system(samtoolsIndex)
	os.system(removesam)

def REDItools(refrence,REDIportal,minAltReads,minDepth,threads,output,REDI):
	REDK=REDI+'/REDItoolKnown.py '
	REDK=REDK+' -i '+output+'/sort.bam -f '+refrence+' -l '+REDIportal+' -t '+str(threads)+' -c '+str(minDepth)+' -T 6-0  -p -e -d -u -m20  -v '+str(minAltReads)+' -n 0.0 -o '+output+'/'+output
	print(REDK)
	os.system(REDK)
	rename='cp '+output+'/'+output+'/'+'*/outTable*'+' '+output+'/'+output+'.REDIRes.txt'
	os.system(rename)

#def AnnotateSNV(toolbox):
#    if not os.path.isfile('mpileup.avinput'):
#		sys.stderr.write("No such file: mpileup.avinput\n")
#		sys.exit(1)
#	Annovar=toolbox+'/annovar/table_annovar.pl '
#	Annovar=Annovar+' mpileup.avinput '+toolbox+'/annovar/humandb/ -buildver hg19  -out AnnotateSNV -protocol Alu,snp138,refGene,RBP_all,cytoBand,dgvMerged,esp6500siv2_all,exac03,genomicSuperDups,gerp++elem,targetScanS,wgRna,phastConsElements100way,phastConsElements46way,rmsk -operation r,f,g,r,r,r,f,f,r,f,r,r,r,r,r   -nastring . -csvout -thread 2 -remove'
#	os.system(Annovar)




def main():
	import argparse
	usage  = "%(prog)s [options]" 
	parser  = argparse.ArgumentParser(usage=usage, description=desc, epilog=epilog, \
                                      formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose")
	parser.add_argument('--version', action='version', version='0.99a')
	parser.add_argument('-o','--output',required=False,  help="where results put")
	parser.add_argument('-R','--REDI',required=False,  help="where REDIknowns.py is")
	parser.add_argument('-i','--input',nargs='*',default=[],required=False,  help="input RNA-seq fastq file")
	parser.add_argument('-r','--refrence',required=False,  help="refrence genome fasta,only for hg19")
	parser.add_argument('-ri','--refrenceIndex',required=False,  help="Hisat2 Index refrence genome fasta,only for hg19")
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
	print("Making output directory...")
	os.system('mkdir '+o.output)
	#os.system('cd '+o.output)
	print("Mapping the reference genome...")
	mapping(o.input,o.refrence,o.refrenceIndex,o.output,o.threads)
	print("Mapping results converting...")
	samtools(o.threads,o.output)
	print("Calling RNA editing events from mapping results...")
	REDItools(o.refrence,o.REDIportal,o.minAltReads,o.minDepth,o.threads,o.output,o.REDI)


if __name__=='__main__': 
	t0 = datetime.now()
	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("\nCtrl-C pressed!      \n")
	dt = datetime.now()-t0
	sys.stderr.write("#Time elapsed: %s\n" % dt)
