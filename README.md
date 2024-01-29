# REDiff: A robust statistical framework for precise assessment of differential RNA editing in limited samples

Introduction
============
<p align-text="justify"> REDiff,  a specialized software for the human species, enables comprehensive RNA editing level analysis from raw fastq files. The tool efficiently prepares reference data, computes editing levels within individual samples, and compares events across distinct groups. False discovery rate correction ensures statistical rigor, enhancing outcome precision and interpretability. Finally, ReDiff provides differentially edited results with detailed annotations.</p>
![](/schema.png)
Installation
============
**for python 2.7:** <br/> <br/> 
<small>conda install anaconda::pandas <br/> <br/> 
conda install anaconda::statsmodels  <br/> <br/> 
conda install scipy <br/> <br/> 
pip install DateTime <br/> <br/> </small>

**for linux:** <br/> <br/> 
<small>conda install bioconda::samtools <br/> <br/> 
conda install bioconda::hisat2 <br/> <br/> </small>


**<small>please copy all scripts of REDiff to /usr/bin/ or your conda eviroment bin local.</small>**


Usage
============
**step0: downloading necessary files for hg19** <br/> <br/> 
**Code:** <small>python2.7 prepareRefrence.py -o test </small><br/> <br/> 
**Output:** <br/> <small>there would be 6 files listed in “test” directory, major 3 parts. <br/>
1). Reference genome sequence, which downloaded from GENCODE. <br/>
2). Snp masked index for hisat2, which integrated by hisat2. <br/></small>
3). RNA editing events downloaded and reformatted from REDIportal. Final disk usage is nearly 11 GB. <br/>
**Parameters:** <br/>  <small>
-o: the output directory name <br/> <br/> </small>

**REDiff step 1: mapping, sorting, and calling RNA editing events** <br/> <br/> 
**Code:** <small> python2.7 CutAndMapping.py -o shADAR_rep1 -i SRR12091801.fastq -ri test/grch37_snp/genome_snp -r test/hg19.ref.fa -k test/hg19_ref/REDIportals.forREDItools.txt.gz -t 64<br/> <br/>  </small>
**Output:** <br/> <small> RNA editing events file, which named by “shADAR_rep1”, which was the standard output files from REDIknown 1.4. This file contained the position of RNA editing, specific number of bases of A, T, C, G, respectively, the average scores and RNA editing levels in this sample. <br/> <br/>  </small>
**Parameters:** <br/> <small>
-o: indicate the output files prefix; <br/>
-i: file names of adapter-trimmed fastq file, two files indicate pair-end sequencing files;  <br/>
-ri: the path of snp masked index for hisat2;  <br/>
-r: the path of reformatted RNA editing database from REDIportal;  <br/>
-t number of threads for mapping, sorting, and calling RNA editing events.<br/> <br/>  </small>
**REDiff step 2: merging, calculating, and annotating significant RNA editing events**<br/> <br/> 
**Code:** <small> <br/> python MergeTable.py -o siADARVsControl -c Huvec_Scrambled_hypoxia_rep1.xls Huvec_Scrambled_hypoxia_rep2.xls Huvec_Scrambled_hypoxia_rep3.xls  -t Huvec_siADAR1_hypoxia_rep1.xls Huvec_siADAR1_hypoxia_rep2.xls Huvec_siADAR1_hypoxia_rep3.xls -k ../ouir/hg19_ref/TABLE1_hg19.forAnnotation.txt  <br/> <br/>  </small>
**Output:**<br/> 
“siADARVsControl.Annotated.csv”, the annotated differential RNA editing events file, This file contained the position of RNA editing, total number of all replicates of base of A, T, C, G, for case and control group, respectively, the differential RNA editing levels between case and control group, the p-value and fdr value for specific RNA editing events. annotation contained the genes, gene region the specific editing sites within. <br/>
“control.REDIMerege.xls” and “treat.REDIMerege.xls”, those were the merge files of replicates withing control and case group. <br/>
**Parameters:** <br/> <small> -o: indicate the output files prefix; <br/>
-c: file names of RNA editing results from control group; <br/>
-t: file names of RNA editing results from case group;<br/>
-k: the path of reformatted RNA editing database from REDIportal, which was for annotation.  </small>

results 
=======

<small> the meaning of each coloumn in the *.Annotated.csv is as below:<br/>
**chr:** the chromosome name;<br/>
**pos:** the position of the editing sites in genome;<br/>
**Ref:** the base of the specific genome position for this site;<br/>
**strand:** the strand of this base belong, 0 means minus strand, 1 meands plus strand;<br/>
**A_treatGroup:** total number of A base in the specific genome  site;<br/>
**C_treatGroup:** total number of C base in the specific genome  site;<br/>
**G_treatGroup:** total number of G base in the specific genome  site;<br/>
**T_treatGroup:** total number of T base in the specific genome  site;<br/>
**A_ControlGroup:** total number of A base in the specific genome  site;<br/>
**C_ControlGroup:** total number of C base in the specific genome  site;<br/>
**G_ControlGroup:** total number of G base in the specific genome  site;<br/>
**T_ControlGroup:** total number of T base in the specific genome  site;<br/>
**delta:** the absolute editing level difference between treat and control group;<br/>
**odd_ratio:** the odd ratio value from fisher test;<br/>
**p_value:** the siginificance p-value value from fisher test;<br/>
**fdr:** the fdr value for the difference level in the specific genome site;<br/>
**Ed~phastConsElements100way:** the annotation from REDIPortals.<br/>  </small>

Authors
=======
Hu Xiaolin<br/>
184514@shsmu.edu.cn<br/>



