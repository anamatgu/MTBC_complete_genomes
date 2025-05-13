## Assembly Quality Control and lift-over

In this section, the different tools for genome assembly assessment are described, as well as the tool used to convert genomic coordinates from the H37Rv reference genome to each genome assembly.

### Assembly Quality Control following the 3C's criterion


### Lift over of H37Rv genomic coordinates 
```
liftoff -g H37Rv.gff3 -o SAMPLE_ASM.gff3 -u SAMPLE.unmapped_features -dir SAMPLE.intermediate_files SAMPLE_ASM.fasta Mycobacterium_tuberculosis_H37Rv_genome.fasta -copies -f additional -overlap 0.2
```
