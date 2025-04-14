#!/usr/bin/bash

: 'This script is for running the hmmIBD to identify 
segments of shared ancestry IBS
'

#paths
vcf=/home/kimani/Desktop/Kilifi_1000_genomes/Data/filtered_Kilifi_1000_snps.vcf.gz

#running the conversion script
: 'input file= vcf, 
expected output = allele.txt, freq.txt, sample.txt
'

if [! -f "$vcf"]; then
	echo "vcf not available"
elif ! command -v python3 &> /dev/null; then
	echo "python3 not availabe"
else 
	python3 vcf2hmm.py $vcf filtered_kilifi
	echo "conversion done"
fi

###running the hmmibd
#input: -i seq.txt -f freq.txt   
#output hmm.txt and hmm_fract.txt
./hmmIBD -i filtered_kilifi_seq.txt  -o filtered_ibs -f filtered_kilifi_freq.txt -m 10

