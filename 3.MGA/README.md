## Multiple Genome Alingment (MGA)
### Construction of MGA

The MGA was constructed following steps with default parameters recommended by [cactus](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md) (v2.8.4)
```
cactus-minigraph jobstore IDs_ASM.txt MGA.sv.gfa --reference MTBCA_ref

cactus-graphmap jobstore IDs_ASM.txt MGA.sv.gfa cactus.paf --outputFasta MGA.sv.gfa.fa --reference MTBCA_ref

cactus-align jobstore IDs_ASM.txt MGA.paf MGA.hal --reference MTBCA_ref --pangenome --outVG --maxLen 10000

cactus-graphmap-join jobstore --vg MGA.vg --outDir MGA_final --outName MGA_final --reference MTBCA_ref --vcf --gfa --gbz --giraffe clip --haplo --odgi

cactus-hal2maf jobstore MGA.hal MGA.maf.gz --refGenome MTBCA_ref --chunkSize 500000 --dupeMode single --noAncestors
```


### Refinement of MGA

The first step to refine the MGA obtained by cactus was the detection of single variants between all the samples in the MGA (SAMPLE_ASM) and the MTBCA reference genome (MTBCA_Ref) using three approaches:

1. From the MGA file using a customized Python script:
```
python3 MTBanc.maf.pairwise.multiprocess.py MGA.maf ids_maf_wcontig
```

2. From single assembly files with minimap2 (alignment) and paftools (variant calling)

```
minimap2 -x asm20 -t 1 -c --cs MTBCA_ref.fasta SAMPLE_ASM.fasta  | sort -k6,6 -k8,8n | minimap_V2.26/bin/paftools.js call -l 50 -L 50 -f MTBCA_ref.fasta - > SAMPLE_ASM_REF.vcf
```

3. From single assembly files with nucmer/dnadiff (alignment and variant calling)

```
dnadiff MTBCA_ref.fasta SAMPLE_ASM.fasta -p prefix
```
Once all single variants were identified, the following script was run to classify them based on the concordance between methods. The file samples_ids_in_maf.txt must contain all the sample IDs in the MGA (maf format), one per row. The files with the results of the variant calling from each approach must match the following names:
```
python3 refine_maf.py samples_ids_in_maf.txt SAMPLE.mga.snps SAMPLE.dnadiff.snps SAMPLE.minimap2.snps
```

Six files were generated:
- equals_error10.refine.snps and equal.refine.snps: positions with SNPs detected by the three approaches
- not_nucmer_not_minimap.refine.snps: positions with SNPs only detected in the MGA approach (mask)
- only_minimap.refine.snps: positions with SNPs detected by MGA and minimap2 approaches
- only_nucmer.refine.snps: positions with SNPs detected by MGA and nucmer/dnadiff approaches
- ambigous_discard.refine.snps: positions with ambiguities of the number of SNPs depending on the approach (mask)

The two files containing the positions to mask were concatenated:
```
cat ambigous_discard.refine.snps not_nucmer_not_minimap.refine.snps | sort -n > SNPsMASK.refine.snps
```

Before the masking step, additional positions to mask were indicated in individual files for each sample in tsv format with these columns without a header:
CONTIG_NAME POSITION WT ALT(alternative allele) DEPTH AF(alternative allele frequency)
Example: contig_1 421150 G T 139 0.258993

In our study, we indicated in these files the positions with non-fixed SNPs (Allele Frequency between 0.1 and 0.9) to exclusively consider fixed SNPs in our downstream analysis. 

```
python3 mask_maf.py sample_ids_HZcalls SNPsMASK.refine.snps MGA.maf
```


### Pairwise genetic distances from MGA

```
python3 all_to_all.mafmasked.pairwise.multiprocess.py MGA_refined.maf sample_ids_maf
```
