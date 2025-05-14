## Multiple Genome Alingment (MGA)
### Construction of MGA

The MGA was constructed 
```
cactus-minigraph jobstore IDs_ASM.txt MGA.sv.gfa --reference MTBCA_ref

cactus-graphmap jobstore IDs_ASM.txt MGA.sv.gfa cactus.paf --outputFasta MGA.sv.gfa.fa --reference MTBCA_ref

cactus-align jobstore IDs_ASM.txt MGA.paf MGA.hal --reference MTBCA_ref --pangenome --outVG --maxLen 10000

cactus-graphmap-join jobstore --vg MGA.vg --outDir MGA_final --outName MGA_final --reference MTBCA_ref --vcf --gfa --gbz --giraffe clip --haplo --odgi

cactus-hal2maf jobstore MGA.hal MGA.maf.gz --refGenome MTBCA_ref --chunkSize 500000 --dupeMode single --noAncestors
```


### Refinement of MGA

Obtener pairwise distance entre MTB ancestor y todas las secuencias (pueden tenerse en cuenta los contigs o no)
```
python3 /data/ana_compartido/PACBIO/scripts_PACBIO/pairwise_distances/MTBanc.maf.pairwise.multiprocess.py cactus_noAnc_final.maf ids_maf_wcontig
```
Obtener pairwise distances con minimap2

```
minimap2 -x asm20 -t 1 -c --cs CCS_G1446.fbAF90.fasta CCS_G1369.fbAF90.fasta | sort -k6,6 -k8,8n | /home/ana/SoftAna/miniconda3/envs/minimap_V2.26/bin/paftools.js call -l 50 -L 50 -f CCS_G1446.fbAF90.fasta - > call.paf

```

Obtener pairwise distance con dnadiff

```
dnadiff /data/ana_compartido/PACBIO/MTB_annotations/MTBancestor_annotation/MTBancestor.fna {}.fasta -p {}-MTBanc
```

Determinar la concordancia entre cactus, dnadiff y minimap2
```
python3 refine_maf_wcontig.py ids_maf_wcontig
```
Unir en una carpeta los snps que vamos a descartar:
```
cat ambigous_discard.refine.snps not_nucmer_not_minimap.refine.snps | sort -n > SNPsMASK.refine.snps
```
QUITAR NOMBRES RAROS DE los contigs de *.change como ‘manual’ y las coordenadas

Crear un archivo con los ids de los assemblies que tienen HZ calls:

(está en el cvs refine)

Correr el script para maskear con Ns las posiciones:
```
python3 ../mask_FP_calls_maf.py ids_HZcalls SNPsMASK.refine.snps
```
Ordenar las secuencias en cada bloque del MAF
```
/home/ana/cactus-bin-v2.8.4/bin/mafRowOrderer -m cactus_noAnc_final_masked.maf --order-file ids_cactus_maflist > cactus_noAnc_final_masked.sorted.maf
```


### Pairwise genetic distances from MGA

```
python3 /data/ana_compartido/PACBIO/scripts_PACBIO/pairwise_distances/all_to_all.mafmasked.pairwise.multiprocess.py cactus_noAnc_final_masked.sorted.1contig.maf ids_maf_1contig
```
