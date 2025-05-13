## Assembly Quality Control and lift-over

In this section, the different tools for genome assembly assessment are described, as well as the tool used to convert genomic coordinates from the H37Rv reference genome to each genome assembly.

### Assembly Quality Control:

```
quast {}.fbAF75.fasta -r /data/Databases/MTB_ancestor/MTB_ancestor_reference.fasta --pacbio /data/ana_compartido/PACBIO/ULTIMATE_ASSEMBLIES/{}.filt.fastq.gz -o {}.quast --features ../H37Rv_annot_TP1_final_checked.gff3 --gene-finding --conserved-genes-finding
```

```
busco -i $SAMPLE.assembly.fasta -l corynebacteriales_odb10 -o $SAMPLE.busco.corynebacteriales -m genome -c 5
```







