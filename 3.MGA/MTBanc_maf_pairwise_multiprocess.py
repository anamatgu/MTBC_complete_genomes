#!/usr/bin/env python3

import sys
import os
from Bio import AlignIO
import itertools
from multiprocessing import Pool

# Parse input files
maf_file = sys.argv[1]
ids = sys.argv[2]

# Load MAF alignments once
alignments = list(AlignIO.parse(maf_file, "maf"))

# Load sample IDs
list_ids = [line.strip().split('\t')[0] for line in open(ids)]

def pairwise(id):
    asm = id
    dic_mut = {}
    
    # Process each alignment block
    for aln in alignments:
        list_ids_block = [seqrec.id for seqrec in aln]
        if 'MTB_ancestor_reference.MTB_anc' in list_ids_block and asm in list_ids_block:
            seq1, seq2, start1, start2, count_gaps_ref, count_gaps_alt = None, None, None, None, 0, 0
            for seqrec in aln:
                if seqrec.id == 'MTB_ancestor_reference.MTB_anc':
                    seq1 = seqrec.seq
                    start1 = seqrec.annotations["start"]
                elif seqrec.id == asm:
                    seq2 = seqrec.seq
                    start2 = seqrec.annotations["start"]

            # If both sequences are available, calculate mutations
            total_length = aln.get_alignment_length()
            for i in range(total_length):
                if seq1[i] == '-':
                    count_gaps_ref += 1
                if seq2[i] == '-':
                    count_gaps_alt += 1
                if seq1[i] != '-' and seq2[i] != '-' and seq1[i] != seq2[i] and seq1[i] != 'N' and seq2[i] != 'N':
                    pos_ref = i - count_gaps_ref + start1 + 1
                    pos_query = i - count_gaps_alt + start2 + 1
                    dic_mut[pos_ref] = [
                        'MTB_anc', str(pos_ref), seq1[i],
                        asm, str(pos_query), seq2[i],
                    ]

    # Write mutations to output file
    filename = f"MTB_anc-{asm}.maf.snps"
    with open(filename, "w") as f:
        for values in dic_mut.values():
            f.write('\t'.join(values) + '\n')


if __name__ == '__main__':
    with Pool(processes=20) as pool:
        pool.map(pairwise, list_ids)
