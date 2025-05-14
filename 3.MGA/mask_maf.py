#!/usr/bin/env python3

import sys
from Bio import AlignIO
from Bio.Seq import MutableSeq, Seq
from Bio.Align import MultipleSeqAlignment
from Bio.AlignIO.MafIO import MafIndex

# Load your MAF alignment file
alignment_file = sys.argv[3]
masked_file = "MGA_masked.maf"

# Load HZ calls files and FP calls files

FPcalls2mask = sys.argv[2]

# Define the positions to mask (Example format)
# The structure is {"sequence_name": [pos1, pos2, ...]}


positions_to_mask = {}
with open(FPcalls2mask, "r") as FPcalls:
	for line in FPcalls:
		linea = line.strip().split()
		pos = int(linea[0])
		samples = linea[4].split(',')
		for sample in samples:
			dic_coords = {}
			with open(sample+'.mga.snps', "r") as maf_snps:
				for line in maf_snps:
					linea = line.strip().split()
					pos_ref, pos_asm = int(linea[1]), int(linea[4])
					dic_coords[pos_ref] = pos_asm
				if sample not in positions_to_mask.keys():
					positions_to_mask[sample] = [int(dic_coords[pos])]
				else:
					positions_to_mask[sample].append(int(dic_coords[pos]))

ids = sys.argv[1]
list_ids = [line.strip() for line in open(ids)]

for sample in list_ids:
	with open(sample+'.Npos.changes', "r") as HZ:
		for line in HZ:
			linea = line.strip().split()
			pos_HZ = int(linea[1])
			sample_contig = sample+'.'+sample+'_'+linea[0]
			if sample_contig not in positions_to_mask.keys():
				positions_to_mask[sample_contig] = [pos_HZ]
			else:
				positions_to_mask[sample_contig].append(pos_HZ)

# Parse the MAF file and modify positions
new_records = []
with open(alignment_file) as maf_file:
	alignment = AlignIO.parse(maf_file, "maf")

	for multiple_alignment in alignment:
        # For each alignment block
		new_block = []

		for record in multiple_alignment:
			seq_name = record.id
			seq_start = int(record.annotations.get("start", 0))
			strand = record.annotations.get("strand", 1)
			seq_len = len(record.seq)
			seq_end = int(seq_start + seq_len)

            # Create a mutable version of the sequence for editing
			mutable_seq = MutableSeq(str(record.seq))

			if seq_name in positions_to_mask:
                # Mask each specified position with 'N'
				for pos in positions_to_mask[seq_name]:
					if seq_start <= int(pos-1) < seq_end:
                        # Calculate the position within the MAF block
						if '-' not in mutable_seq:
							#block_pos = int(pos-1) - int(seq_start) if int(strand) == 1 else int(seq_end) - int(pos-1) -1
							block_pos = int(pos-1) - int(seq_start)
							mutable_seq[block_pos] = 'N'
						else:
							block_pos = 0
							non_gap_count = 0
							for i, base in enumerate(mutable_seq):
								if base != "-":
									if seq_start + non_gap_count == pos-1:
										block_pos = i
										break
									non_gap_count += 1
							mutable_seq[block_pos] = 'N'

            # Create a new record with the modified sequence
			record.seq = Seq(str(mutable_seq))
			new_block.append(record)

        # Add modified block to the list of new records
		new_alignment_block = MultipleSeqAlignment(new_block)
		new_records.append(new_alignment_block)

# Write modified alignment to a new MAF file
with open(masked_file, "w") as output_maf:
	AlignIO.write(new_records, output_maf, "maf")
