#!/usr/bin nextflow
/* 
This is a script foe runnning ibd for kilifi population
*/
params.vcf="/home/kimani/Desktop/1000_genomes/hmmIBD/data/subset_Kilifi_1000_snps.vcf.gz"
params.vcfscript="/home/kimani/Desktop/1000_genomes/hmmIBD/vcf2hmm.py"
params.hmmibd= "/home/kimani/Desktop/1000_genomes/hmmIBD/"
params.outdir="/home/kimani/Desktop/1000_genomes/hmmIBD/Results"

process conversion{
    publishDir "${params.outdir}/conversion", mode:"copy"
    tag "$vcf"

    input:
    path vcfscript
    path vcf

    output:
    path "*_seq.txt"  , emit: seq_file
    path "*_freq.txt"  , emit: freq_file


    script:
    """
    python3 ${vcfscript} ${vcf} filtered_kilifi
    """
}

process hmmibd{
    publishDir "${params.outdir}/hmmIBD", mode:"copy"
    input:
    path hmmibd
    path seq_file
    path freq_file

    output:
    path "*.hmm.txt", emit: hmm_file
    path "*hmm_fract.txt", emit: hmm_fract


    script:
    """
    ${hmmibd}/hmmIBD -i ${seq_file} -o filtered_ibs -f ${freq_file} -m 10
    """
}



// workflow
workflow{
    //conversion process from vcf
    vcf_ch = Channel.fromPath(params.vcf)
    script_ch = Channel.fromPath(params.vcfscript)
    
   conv= conversion(script_ch ,vcf_ch)
   conv.seq_file.view()
   conv.freq_file.view()

//running the identity by descent
    //seq=conv.conv_output.map{ it[2] }
    //freq=conv.conv_output.map { it[1] }
    hmmibd_ch= Channel.fromPath(params.hmmibd)
    
    hmm=hmmibd(hmmibd_ch,  conv.seq_file, conv.freq_file  )

    hmm.hmm_file.view()
    hmm.hmm_fract.view()

}