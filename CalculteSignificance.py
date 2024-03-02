#!/usr/bin/env python

from __future__ import division
import os,sys,re
import pandas as pd
from datetime import datetime
import scipy.stats as stats
from statsmodels.stats.multitest import fdrcorrection as fdr
import warnings
warnings.filterwarnings('ignore')

desc="""this file is the core file to detection differential RNA editing events between different groups. firstly, RNA editing events adn editing levels from all replicates in the same group would merged. here, we combine reads for different base (ATCG) and recaculate RNA editing levels with the number of base G and base A. second, the siginificance of specific editing events are valuved with fisher test, which we had introduced in our previous study. to minimize the false positive sites here, FDR were used. Finally, we use the annotaion from REDIportal to annoate RNA editing events we identified. 


"""
epilog="""Author: Hu Xiaolin
15216716554@163.com

Shanghai/China 10/10/2023
"""




def mergeFiles(files,prefix):
	fileNames=''
	for file in files:
		fileNames=fileNames+' '+file
	print(prefix+': '+fileNames)
	os.system("head -n 1 "+files[0] +"| sed 's/\[//g' | sed 's/\]//g' | sed 's/, /\t/g' | sed 's/,/\t/g' > "+prefix+'.REDIMerege.xls')
	os.system("cat "+fileNames+" | sed 's/\[//g' | sed 's/\]//g' | sed 's/, /\t/g' | sed 's/,/\t/g' | grep -v 'Region'>> "+prefix+'.REDIMerege.xls')
	data=pd.read_table(prefix+'.REDIMerege.xls',sep="\t",header=0, low_memory=False)
	data2=pd.DataFrame(data, columns=['Region','Position','Strand','BaseCountA','C','G','T'])
	del data
	data2['id']=data2['Region'].map(str)+"@"+data2['Position'].map(str)+"@"+data2['Strand'].map(str)
	data_frame=pd.DataFrame()
	data_frame['A'] = data2['BaseCountA'].map(int).groupby(data2['id']).sum()
	data_frame['C'] = data2['C'].map(int).groupby(data2['id']).sum()
	data_frame['G'] = data2['G'].map(int).groupby(data2['id']).sum()
	data_frame['T'] = data2['T'].map(int).groupby(data2['id']).sum()
	data_frame['ID']=data_frame.index.values
	del data2
	return data_frame

def calculateDE(MergedFile):
	i=0
	while(i < len(MergedFile)):
		delta=MergedFile.at[i,'G_x']/(MergedFile.at[i,'A_x']+MergedFile.at[i,'G_x'])-MergedFile.at[i,'G_y']/(MergedFile.at[i,'A_y']+MergedFile.at[i,'G_y'])
		odd_ratio, p_value = stats.fisher_exact([[MergedFile.at[i,'G_x'],MergedFile.at[i,'A_x']+MergedFile.at[i,'G_x']],[MergedFile.at[i,'G_y'],MergedFile.at[i,'A_y']+MergedFile.at[i,'G_y']]])
		MergedFile.at[i,'delta']=delta
		MergedFile.at[i,'odd_ratio']=odd_ratio
		MergedFile.at[i,'p_value']=p_value
		i=i+1
		if(i % 10000 ==0):
			remaining=len(MergedFile)-i
			print('\r',str(remaining)+" remaining...", end='', flush=True)
	rej,FDR=fdr(MergedFile['p_value'])
	MergedFile['fdr']=FDR
	order=['ID','A_x','C_x','G_x','T_x','A_y','C_y','G_y','T_y','delta','odd_ratio','p_value','fdr']
	MergedFile=MergedFile[order]
	MergedFile[['chr', 'pos', 'strand']] = MergedFile['ID'].str.split('@', 2, expand = True)
	return MergedFile

def annotate(MergedFile,reference):
	ref=pd.read_table(reference,sep="\t",header=0, low_memory=False)
	ref['ID']=ref['Region'].map(str)+"@"+ref['Position'].map(str)+"@"+ref['Strand'].map(str)
	Annotaed=pd.merge(MergedFile,ref,on='ID',how="inner")
	orderNew=['ID','chr','pos','Ref','strand','A_x','C_x','G_x','T_x','A_y','C_y','G_y','T_y','delta','odd_ratio','p_value','fdr','Region','Position','Strand','Ed','db','type','dbsnp','repeat','Func.wgEncodeGencodeBasicV34lift37','Gene.wgEncodeGencodeBasicV34lift37','GeneDetail.wgEncodeGencodeBasicV34lift37','ExonicFunc.wgEncodeGencodeBasicV34lift37','AAChange.wgEncodeGencodeBasicV34lift37','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','Func.knownGene','Gene.knownGene','GeneDetail.knownGene','ExonicFunc.knownGene','AAChange.knownGene','phastConsElements100way']
	Annotaed=Annotaed[orderNew]
	Annotaed.rename(columns={'A_x':'A_treatGroup','C_x':'C_treatGroup','G_x':'G_treatGroup','T_x':'T_treatGroup','A_y':'A_ControlGroup','C_y':'C_ControlGroup','T_y':'T_ControlGroup','G_y':'G_ControlGroup'},inplace=True)
	#Annotaed=Annotaed.
	return Annotaed.drop(['ID', 'Region','Position','Strand'], axis=1)



def main():
	import argparse
	usage  = "%(prog)s [options]" 
	parser  = argparse.ArgumentParser(usage=usage, description=desc, epilog=epilog, \
                                      formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-o", "--output", default="hg19_ref2", help="output file names (CSV)")
	parser.add_argument("-t", "--treat",nargs='*',default=[], help="filelist for treatment/case group")
	parser.add_argument("-c", "--control",nargs='*',default=[], help="filelist for control group")
	parser.add_argument("-k", "--REDIportal",required=False,default='no',  help="path to REDIportal databases,for annotation")
	parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose")

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	o = parser.parse_args()
	if o.verbose:
		sys.stderr.write("Options: %s\n"%str(o))
	treatfiles=o.treat
	for file in treatfiles:
		if not os.path.isfile(file):
			sys.stderr.write("No such file: %s\n"%file)
			sys.exit(1)
	controlfiles=o.control
	for file in controlfiles:
		if not os.path.isfile(file):
			sys.stderr.write("No such file: %s\n"%file)
			sys.exit(1)
	print("Merging...")
	Treat=mergeFiles(treatfiles,'Treat')
	Control=mergeFiles(controlfiles,'Control')
	TC_table=pd.merge(Treat,Control,on='ID',how="inner")
	print("\nCaculating DE...")
	out=calculateDE(TC_table)
	out.to_csv(o.output+".csv",index=False,sep=',')
	if(o.REDIportal != 'no' and os.path.isfile(o.REDIportal)):
		print("\n\nAnnotating...")
		Anno=annotate(out,o.REDIportal)
		Anno.to_csv(o.output+".Annotated.csv",index=False,sep=',')
		Anno[Anno['fdr'] <0.3].to_csv(o.output+".Annotated_FDRfilter.csv",index=False,sep=',')


if __name__=='__main__': 
	t0 = datetime.now()
	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("\nCtrl-C pressed!      \n")
	dt = datetime.now()-t0
	sys.stderr.write("#Time elapsed: %s\n" % dt)
