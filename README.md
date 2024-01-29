# REDiff：python scripts for identifying differential RNA editing events between different groups with small size RNA-seq dataset.

Introduction
============
<p align-text="justify"> ReDiff,  specialized software for the human species, enables comprehensive RNA editing level analysis from raw fastq files. The tool efficiently prepares reference data, computes editing levels within individual samples, and compares events across distinct groups. False discovery rate correction ensures statistical rigor, enhancing outcome precision and interpretability. Finally, ReDiff provides differentially edited results with detailed annotations.</p>

Installation
============
**for python 2.7:** <br/> <br/> 
conda install anaconda::pandas <br/> <br/> 
conda install anaconda::statsmodels  <br/> <br/> 
conda install scipy <br/> <br/> 
pip install DateTime <br/> <br/> 

**for linux:** <br/> <br/> 
conda install bioconda::samtools <br/> <br/> 
conda install bioconda::hisat2 <br/> <br/> 

**please copy all scripts of REDiff to /usr/bin/ or your conda eviroment bin local.**

Usage
============
**step0: downloading necessary files for hg19** <br/> <br/> 
**Code:** python2.7 prepareRefrence.py -o test <br/> <br/> 
**Output:** there would be 6 files listed in “test” directory, major 3 parts. <br/>
1). Reference genome sequence, which downloaded from GENCODE. <br/>
2). Snp masked index for hisat2, which integrated by hisat2. <br/>
3). RNA editing events downloaded and reformatted from REDIportal. Final disk usage is nearly 11 GB. <br/>
**Parameters:** <br/> 
-o: the output directory name <br/> <br/> 

**ReDiff step 1: mapping, sorting, and calling RNA editing events** <br/> <br/> 
**Code:** python2.7 CutAndMapping.py -o shADAR_rep1 -i SRR12091801.fastq -ri test/grch37_snp/genome_snp -r test/hg19.ref.fa -k test/hg19_ref/REDIportals.forREDItools.txt.gz -t 64<br/> <br/>
**Output:** RNA editing events file, which named by “shADAR_rep1”, which was the standard output files from REDIknown 1.4. This file contained the position of RNA editing, specific number of bases of A, T, C, G, respectively, the average scores and RNA editing levels in this sample. <br/> <br/>
**Parameters:**
-o: indicate the output files prefix; <br/>
-i: file names of adapter-trimmed fastq file, two files indicate pair-end sequencing files;  <br/>
-ri: the path of snp masked index for hisat2;  <br/>
-r: the path of reformatted RNA editing database from REDIportal;  <br/>
-t number of threads for mapping, sorting, and calling RNA editing events.<br/> <br/>
**ReDiff step 2: merging, calculating, and annotating significant RNA editing events**<br/> <br/> 
**Code:** python MergeTable.py -o siADARVsControl -c Huvec_Scrambled_hypoxia_rep1.xls Huvec_Scrambled_hypoxia_rep2.xls Huvec_Scrambled_hypoxia_rep3.xls  -t Huvec_siADAR1_hypoxia_rep1.xls Huvec_siADAR1_hypoxia_rep2.xls Huvec_siADAR1_hypoxia_rep3.xls -k ../ouir/hg19_ref/TABLE1_hg19.forAnnotation.txt  <br/> <br/>
**Output:**<br/> 
“siADARVsControl.Annotated.csv”, the annotated differential RNA editing events file, This file contained the position of RNA editing, total number of all replicates of base of A, T, C, G, for case and control group, respectively, the differential RNA editing levels between case and control group, the p-value and fdr value for specific RNA editing events. annotation contained the genes, gene region the specific editing sites within. <br/>
“control.REDIMerege.xls” and “treat.REDIMerege.xls”, those were the merge files of replicates withing control and case group. <br/>
**Parameters:** -o: indicate the output files prefix; <br/>
-c: file names of RNA editing results from control group; <br/>
-t: file names of RNA editing results from case group;<br/>
-k: the path of reformatted RNA editing database from REDIportal, which was for annotation.

results 
=======

the meaning of each coloumn in the *.Annotated.csv is as below:
**chr:** the chromosome name;
**pos:** the position of the editing sites in genome;
**Ref:** the base of the specific genome position for this site;
**strand:** the strand of this base belong, 0 means minus strand, 1 meands plus strand;
**A_treatGroup:** total number of A base in the specific genome  site;
**C_treatGroup:** total number of C base in the specific genome  site;
**G_treatGroup:** total number of G base in the specific genome  site;
**T_treatGroup:** total number of T base in the specific genome  site;
**A_ControlGroup:** total number of A base in the specific genome  site;
**C_ControlGroup:** total number of C base in the specific genome  site;
**G_ControlGroup:** total number of G base in the specific genome  site;
**T_ControlGroup:** total number of T base in the specific genome  site;
**delta:** the absolute editing level difference between treat and control group;
**odd_ratio:** the odd ratio value from fisher test;
**p_value:** the siginificance p-value value from fisher test;
**fdr:** the fdr value for the difference level in the specific genome site;
**Ed~phastConsElements100way:** the annotation from REDIPortals.



