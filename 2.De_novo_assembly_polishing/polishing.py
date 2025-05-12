#!/usr/bin/env python

import vcf
import sys
from Bio import SeqIO
import subprocess

vcf_file=sys.argv[1]
original_fasta=sys.argv[2]
sample=vcf_file.split('.')[0]

#Filter the original vcf file from freebayes to include the variants with Allele Frequency (AF) above 0.5 that will be introduced in the consensus assembly
##Header of the new vcf
seq_genome = SeqIO.parse(original_fasta, "fasta")
lines_vcf2normal = ['##fileformat=VCFv4.2']
define_reference = '##reference=' + original_fasta
lines_vcf2normal.append(define_reference)
for recordseq in seq_genome:
                this_contig = recordseq.id
                length_seq = len(recordseq.seq)
                define_contig = '##contig=<ID=' + this_contig + ',length=' + str(length_seq) + '>'
                lines_vcf2normal.append(define_contig)
lines_vcf2normal.append('##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth at the locus">')
lines_vcf2normal.append('##INFO=<ID=AF,Number=A,Type=Float,Description="Estimated allele frequency in the range (0,1]">')
lines_vcf2normal.append('#CHROM' + '\t' + 'POS' + '\t' + 'ID' + '\t' + 'REF' + '\t' + 'ALT' + '\t' + 'QUAL' + '\t' + 'FILTER' + '\t' + 'INFO')


##Calculate the alelle frequency and filter consensus variants
for record in vcf.Reader(open(sys.argv[1], 'r')):
	chrom, position, ref, alt  = record.CHROM, record.POS, record.REF, record.ALT
	depth, genotype = record.samples[0]["DP"], record.samples[0]["GT"]
	AO = record.samples[0]["AO"]
	RO = record.samples[0]["RO"]
	AD = record.samples[0]["AD"]
	for i in range(1, len(AD)):
		AFalt = float(AD[i]) / (float(AD[i]) + float(RO)) ###Calculate allele frequency
		alternative = alt[i-1]
		ADtotal = sum(AD)
		if AFalt > 0.50 and ADtotal >= 3: ###Include only the variants with AF > 50
			info_line_vcf = str(chrom) + '\t' + str(position) + '\t' + '.' + '\t' + str(ref) + '\t' + str(alternative) + '\t' + '.' + '\t' + 'PASS' + '\t' + 'DP=' + str(depth) + ';' + 'AF=' + str(AFalt)
			lines_vcf2normal.append(info_line_vcf)

##Create the vcf file with the filtered variants
filename_vcf = sample + '.fbAF50.2vt.vcf'
f0 = open(filename_vcf, 'w')
print >> f0, '\n'.join(lines_vcf2normal)
f0.close()

##Normalize the output from freebayes
filename_vt = sample + '.fbAF50.nv.vcf'
subprocess.call(['/path/to/vt/vt', 'normalize', filename_vcf, '-r', original_fasta, '-q', '-o', filename_vt])



#Parse the filtered vcf with the consensus variants
merge_contigs_list = []
all_changes_list = []


seq_genome2 = SeqIO.parse(original_fasta, "fasta")
for recordseq2 in seq_genome2:
	list_seq = list(recordseq2.seq)
	header = '>' + sample + '_' + recordseq2.id
	this_contig = recordseq2.id
	list_callsAF50 = []

	for line in open(filename_vt, 'r'):
		if '#' not in line:
			linea = line.strip().split()
			CHROM, POS, REF, ALT, DP, AF = linea[0], linea[1], linea[3], linea[4], linea[7].split(';')[0].replace('DP=', ''), linea[7].split(';')[1].replace('AF=', '')
			if CHROM == this_contig:
				if float(AF) >= 0.50:
					info_line = [CHROM, int(POS), str(REF), str(ALT), int(DP), float(AF)]
					list_callsAF50.append(info_line)

#Create the consensus assembly introducing the consensus variants
	for change in list_callsAF50:
		CHROM, POS, REF, ALT, DP, AFalt = change
		nuc_REF = list(REF)
		nuc_ALT = list(ALT)
		if len(nuc_ALT) < len(nuc_REF) and len(nuc_ALT) == 1: #deletions
			for pos in range(int(POS), int(POS)+len(nuc_REF)-1):
				list_seq[pos] = '-'
		elif len(nuc_ALT) > len(nuc_REF) and len(nuc_REF) == 1: #insertions
				list_seq[int(POS)-1] = ALT
		elif len(nuc_ALT) == len(nuc_REF): #SNPs
			if len(nuc_REF) == 1:
				list_seq[int(POS)-1] = ALT
			else:
				for nuc in range(0, len(nuc_REF)):
					if nuc_REF[nuc] != nuc_ALT[nuc]:
						list_seq[int(POS) + int(nuc) - 1] = ALT

	Nlist_noIns = []
	Nlist_insertions = []

#Print the consensus assembly and the changes
	if '-' in list_seq:
		remove_del_list_seq = [i for i in list_seq if i != '-']
	else:
		remove_del_list_seq = list_seq
	merge_insertions_list = ''.join(remove_del_list_seq)
	final_list_seq = list(merge_insertions_list)
	ultimate_list = '\n'.join([''.join(final_list_seq[n:n+80]) for n in range(0, len(final_list_seq), 80)])
	merge_contigs_list.append(header)
	merge_contigs_list.append(ultimate_list)

	list_of_list_changes = '\n'.join(' '.join(map(str,sl)) for sl in list_callsAF50)
	all_changes_list.append(list_of_list_changes)


filename = sample + '.fbAF50.fasta'
f1 = open(filename,'w')
print >> f1, '\n'.join(merge_contigs_list)
f1.close()

filename2 = sample + '.fbAF50.changes'
f2 = open(filename2, 'w')
print >> f2, '\n'.join(all_changes_list)
f2.close()
