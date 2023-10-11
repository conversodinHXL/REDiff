desc="""This script is for process multi-samples parralley, thus reduce the work for large sample size. example of input file is as below:


"""
epilog="""Author: Hu Xiaolin
15216716554@163.com

Shanghai/China 10/10/2023
"""
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import os,sys
from datetime import datetime

def worker(line,o):
	lines=line.split("*")
	#filename=lines[0].split("\t")
	ref= o.refrence
	#print ref
	STARref=o.refrenceIndex
	tb= o.toolbox
	threads= o.threads
	skips=o.skip
	#print skips
	GATK='python  CutAndMapping.py -r '
	GATK=GATK+ref+' -i '+lines[0]+'.fastq '+lines[1]+'.fastq -T '+tb+' -t '+str(threads)+' -o '+str(lines[2])+' -ri '+STARref
	
	#print GATK
	os.system(GATK)
#
def main():
	import argparse
	usage  = "%(prog)s [options]" 
	parser  = argparse.ArgumentParser(usage=usage, description=desc, epilog=epilog, \
                                      formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-r','--refrence',required=True,  help="refrence genome fasta,only for hg19")
	parser.add_argument('-ri','--refrenceIndex',required=True,  help="STAR Index refrence genome fasta,only for hg19")
	parser.add_argument('--version', action='version', version='0.99a')
	parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose")
	#parser.add_argument('-o','--output',required=True,  help="where results put")
	parser.add_argument('-l','--files',required=True,  help="input RNA-seq fastq list")
	parser.add_argument("-t", "--threads", default=4, type=int, help="number of cores to use [%(default)s]")
	parser.add_argument('-k', '--skip', nargs='*',default=[], help="skip process,only cutting,mapping,samtools,mpileUp,AnnotateSNV can be input")
	parser.add_argument("-n", "--thread", default=4, type=int, help="number of cores to use [%(default)s]")
	parser.add_argument('-T','--toolbox',required=True,  help="where tools are")
	
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	o = parser.parse_args()
	if o.verbose:
		sys.stderr.write("Options: %s\n"%str(o))

	pool = multiprocessing.Pool(processes=o.thread)
	for line in open(o.files):
		line=line.strip('\n')
		print(line)
		pool.apply_async(worker, (line,o,))


	pool.close()
	pool.join()

if __name__=='__main__': 
	t0 = datetime.now()
	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("\nCtrl-C pressed!      \n")
	dt = datetime.now()-t0
	sys.stderr.write("#Time elapsed: %s\n" % dt)