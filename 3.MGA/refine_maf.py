#!urs/bin/env/ python3

import sys

ids = sys.argv[1]

list_ids = [line.strip() for line in open(ids)]


maf_dic = {}
dnadiff_dic = {}
minimap_dic = {}


for sample in list_ids: ##Parsing the three SNP files from different approaches
	with open(sample + '.mga.snps', "r") as maf:
		for line in maf:
			linea = line.strip().split()
			pos_maf = int(linea[1])
			if pos_maf not in maf_dic.keys():
				maf_dic[pos_maf] = [sample]
			else:
				maf_dic[pos_maf].append(sample)
	with open(sample + '.dnadiff.snps', "r") as dnadiff:
		for line in dnadiff:
			linea = line.strip().split()
			if linea[1] != '.' and linea[2] != '.':
				pos_dnadiff = int(linea[0])
				if pos_dnadiff not in dnadiff_dic.keys():
					dnadiff_dic[pos_dnadiff] = [sample]
				else:
					dnadiff_dic[pos_dnadiff].append(sample)
	with open(sample + '.minimap2.snps', "r") as minimap:
		for line in minimap:
			if not line.startswith('#'):
				linea = line.strip().split()
				if len(linea[3]) == 1 and len(linea[4]) == 1:
					pos_minimap = int(linea[1])
					if pos_minimap not in minimap_dic.keys():
						minimap_dic[pos_minimap] = [sample]
					else:
						minimap_dic[pos_minimap].append(sample)

final_dic = {}
for pos, samples in maf_dic.items(): ##Determine the concordance between approaches and generate output files
	count_dnadiff = 0
	count_minimap = 0
	if pos in dnadiff_dic.keys():
		for sample in samples:
			if sample in dnadiff_dic[pos]:
				count_dnadiff += 1
	if pos in minimap_dic.keys():
		for sample in samples:
			if sample in minimap_dic[pos]:
				count_minimap += 1
	final_dic[pos] = [str(len(samples)), str(count_dnadiff), str(count_minimap), ','.join(samples)]
	if len(samples) != count_dnadiff or len(samples) != count_minimap:
		if count_dnadiff == 0 and count_minimap == 0:
			with open('not_nucmer_not_minimap.refine.snps', 'a') as both00:
				both0 = str(pos) + '\t' + '\t'.join(final_dic[pos]) + '\n'
				both00.write(both0)
		else:
			error_rate = round(len(samples)*0.1)
			if (len(samples) == count_minimap or (len(samples)-error_rate <= count_minimap <= len(samples)+error_rate)) and count_dnadiff == 0:
				with open('only_minimap.refine.snps', 'a') as only_minimap:
					minimap = str(pos) + '\t' + '\t'.join(final_dic[pos]) + '\n'
					only_minimap.write(minimap)
			elif (len(samples) == count_dnadiff or (len(sample)-error_rate <= count_dnadiff <= len(samples)+error_rate)) and count_minimap == 0:
				with open('only_nucmer.refine.snps', 'a') as only_nucmer:
					nucmer = str(pos) + '\t' + '\t'.join(final_dic[pos]) + '\n'
					only_nucmer.write(nucmer)
			else:
				if (len(samples)-error_rate <= count_dnadiff <= len(samples)+error_rate) or (len(samples)-error_rate <= count_minimap <= len(samples)+error_rate):
					with open('equals_error10.refine.snps', 'a') as equals_error:
						error5 = str(pos) + '\t' + '\t'.join(final_dic[pos]) + '\n'
						equals_error.write(error5)
				else:
					with open('ambigous_discard.refine.snps', 'a') as ambigous:
						amb = str(pos) + '\t' + '\t'.join(final_dic[pos]) + '\n'
						ambigous.write(amb)
	else:
		with open('equal.refine.snps', 'a') as equals:
			equals_print = str(pos) + '\t' + '\t'.join(final_dic[pos]) + '\n'
			equals.write(equals_print)
