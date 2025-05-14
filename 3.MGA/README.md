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

First steps to refine the MGA obtained by cactus were detecting single variants between the assembly (SAMPLE_ASM) and the MTBCA reference genome (MTBCA_Ref) using three approaches:

1. From the MGA file using a customized Python script:
```
python3 MTBanc.maf.pairwise.multiprocess.py MGA.maf ids_maf_wcontig
```

2. From single assembly files with minimap2 (alignment) and paftools (variant calling)

```
minimap2 -x asm20 -t 1 -c --cs MTBCA_ref.fasta SAMPLE_ASM.fasta  | sort -k6,6 -k8,8n | minimap_V2.26/bin/paftools.js call -l 50 -L 50 -f MTBCA_ref.fasta - > SAMPLE_ASM_REF.asm20.vcf
```

3. From dnadiff (alignment and variant calling)

```
dnadiff MTBCA_ref.fasta SAMPLE_ASM.fasta -p prefix
```
Once all single variants were identified, the following script was run to classify the variants depending on the concordances between methods. It generates four files: .a

```
python3 refine_maf_wcontig.py ids_maf_wcontig

cat ambigous_discard.refine.snps not_nucmer_not_minimap.refine.snps | sort -n > SNPsMASK.refine.snps
```
Before refine 
Crear un archivo con los ids de los assemblies que tienen HZ calls:

(está en el cvs refine)

Correr el script para maskear con Ns las posiciones:
```
python3 mask_FP_calls_maf.py sample_ids_HZcalls SNPsMASK.refine.snps
```


### Pairwise genetic distances from MGA

```
python3 all_to_all.mafmasked.pairwise.multiprocess.py MGA_refined.maf sample_ids_maf
```
