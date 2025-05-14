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
pairs_list = list(itertools.combinations(list_ids, 2))

def pairwise(pair):
    asm1, asm2 = pair
    dic_mut = {}
    HF_file = f"{asm1.split('.')[0]}-{asm2.split('.')[0]}.HF.snps"

    # Process each alignment block
    for aln in alignments:
        list_ids_block = [seqrec.id for seqrec in aln]
        if asm1 in list_ids_block and asm2 in list_ids_block:
            seq1, seq2, start1, start2, count_gaps_ref, count_gaps_alt, count_gaps_anc = None, None, None, None, 0, 0, 0
            for seqrec in aln:
                if seqrec.id == asm1:
                    seq1 = seqrec.seq
                    start1 = seqrec.annotations["start"]
                elif seqrec.id == asm2:
                    seq2 = seqrec.seq
                    start2 = seqrec.annotations["start"]

            # If both sequences are available, calculate mutations
            total_length = aln.get_alignment_length()
            for i in range(total_length):
                if aln[0][i] == '-':
                    count_gaps_anc += 1
                if seq1[i] == '-':
                    count_gaps_ref += 1
                if seq2[i] == '-':
                    count_gaps_alt += 1
                if seq1[i] != '-' and seq2[i] != '-' and seq1[i] != seq2[i] and seq1[i] != 'N' and seq2[i] != 'N':
                    pos_ref = i - count_gaps_ref + start1 + 1
                    pos_query = i - count_gaps_alt + start2 + 1
                    pos_anc = i - count_gaps_anc + aln[0].annotations["start"] + 1
                    dic_mut[pos_ref] = [
                        asm1.split('.')[0], str(pos_ref), seq1[i],
                        asm2.split('.')[0], str(pos_query), seq2[i],
                        aln[0].id.split('.')[0], str(pos_anc), aln[0][i]
                    ]

    # Write mutations to output file
    filename = f"{asm1.split('.')[0]}-{asm2.split('.')[0]}.maf.snps"
    with open(filename, "w") as f:
        for values in dic_mut.values():
            f.write('\t'.join(values) + '\n')

if __name__ == '__main__':
    with Pool(processes=22) as pool:
        pool.map(pairwise, pairs_list)
