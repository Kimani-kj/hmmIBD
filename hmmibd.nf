#!/usr/bin nextflow
/* 
This is a script foe runnning ibd for kilifi population
*/
params.vcf="/home/kimani/Desktop/1000_genomes/hmmIBD/data/subset_Kilifi_1000_snps.vcf.gz"
params.vcfscript="/home/kimani/Desktop/1000_genomes/hmmIBD/vcf2hmm.py"
params.hmmibd= "/home/kimani/Desktop/1000_genomes/hmmIBD/"

process conversion{
    tag "$vcf"

    input:
    path vcfscript
    path vcf

    output:
    path "*txt"  , emit: conv_output


    script:
    """
    python3 ${vcfscript} ${vcf} filtered_kilifi
    """
}

process hmmibd{
    
    input:
    path hmmibd
    path seq
    path freq

    output:
    path "*txt", emit: hmmibd_output


    script:
    """
    ${hmmibd}/hmmIBD -i ${seq} -o filtered_ibs -f ${freq} -m 10
    """
}

// workflow
workflow{
    //conversion process from vcf
    vcf_ch = Channel.fromPath(params.vcf)
    script_ch = Channel.fromPath(params.vcfscript)
    
   conv= conversion(script_ch ,vcf_ch)
   conv.conv_output.view()

//running the identity by descent
    seq=conv.conv_output.map{ it[2] }
    freq=conv.conv_output.map { it[1] }
    hmmibd_ch= Channel.fromPath(params.hmmibd)
    
    hmmibd(hmmibd_ch,  seq, freq )


}