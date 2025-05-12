#!/usr/bin/env python

import glob
import pysam
import os

for filename in glob.glob(os.getcwd()+"/*.eqx.sam"):
    samfile = pysam.AlignmentFile(filename, 'r')
    samplename = filename.split('/')[-1].replace('.eqx.sam', '')
    for read in samfile:
        if read.flag != 4 and read.flag != 2048 and read.flag != 2064: ##Remove unmapped reads and supplementary alignments
            snpsperead = 0
            clipped_bases = 0
            insperead = 0
            delperead = 0
            for tupla in read.cigar: ##Count the number of mismatches due to SNPs, insertions or deletions
                if tupla[0] == 8:
                    snpsperead += tupla[1]
                    if tupla[0] == 4:
                        clipped_bases += tupla[1]
                if tupla[0] == 1:
                    insperead += tupla[1]
                if tupla[0] == 2:
                    delperead += tupla[1]
            length = read.infer_query_length(always=False) ##Obtain total read length
            total_len = float(length) - float(clipped_bases) ##Obtain read length without clipped bases 
            error_rate_snps = float(snpsperead)/float(total_len) ##Calculate mismatch rate considering SNPs
            mismatches = snpsperead + insperead + delperead ##Total number of mismatches
            error_rate_total = float(mismatches)/float(total_len) ##Calculate mismatch rate considering all type of mismatches
            indels = insperead + delperead
            print(samplename, read.qname, read.pos, snpsperead, indels, total_len, error_rate_snps, error_rate_total, sep = ',')
