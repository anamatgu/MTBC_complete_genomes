## _De novo_ assembly, polishing and lift-over

### _De novo_ assembly with Flye
Once the long reads were filtered, _de novo_ assembly was performed with [Flye](https://github.com/mikolmogorov/Flye) (v2.9.2) with two polishing iterations:

```
flye --pacbio-hifi SAMPLE.fastq.gz --out-dir SAMPLE_ASM.flye --genome-size 4.5m --threads 15 --iterations 2
```

Then, assemblies were closed with circlator and the start of the genome was fixed according to the _dnaA_ coordinates from H37Rv reference genome (GenBank accession: AL123456.3)

```
circlator all --assembler canu SAMPLE_ASM.fasta SAMPLE.fastq.gz SAMPLE_ASM.circlator --genes_fa H37Rv_dnaA.fa --threads 4
```


### Customized polishing with long reads

The correction of the errors introduced during the assembling or circularization process was performed in two steps:

1. To identify the potential errors, long reads were mapped against their assembly with [pbmm2](https://github.com/PacificBiosciences/pbmm2) (v1.13), variant calling was performed with [freebayes](https://github.com/freebayes/freebayes) (v1.3.6), and the variants were normalized with [vt](https://genome.sph.umich.edu/wiki/Vt) (v0.57721)

```
pbmm2 align SAMPLE_ASM.fasta SAMPLE.fastq SAMPLE_ASM_LRS.sort.bam --preset CCS --sort --sample SAMPLE --rg '@RG\tID:mXXXXX\tSM:mysample'

samtools faidx SAMPLE_ASM.fasta

freebayes -f SAMPLE_ASM.fasta -m 0 --min-coverage 3 -R 0 -p 1 -F 0.1 -E -1 -b SAMPLE_ASM_LRS.sort.bam --vcf SAMPLE.AF10.vcf

cat SAMPLE.AF10.vcf | vt normalize - -r SAMPLE.fasta -q > SAMPLE.vt.AF10.vcf; done
```
2. The following script was customized to introduce the validated changes in the assembly. To successfully run this script, the path to vt must be define in the code.

```
python polishing.py SAMPLE.vt.AF10.vcf SAMPLE_ASM.fasta
```


### Lift over of H37Rv genomic coordinates

To convert the genomics coordinates from H37Rv to each assembly the [liftoff tool](https://github.com/agshumate/Liftoff) (v1.6.3) was used with the following parameters:

```
liftoff -g H37Rv.gff3 -o SAMPLE_ASM.gff3 -u SAMPLE.unmapped_features -dir SAMPLE.intermediate_files SAMPLE_ASM.fasta Mycobacterium_tuberculosis_H37Rv_genome.fasta -copies -f additional -overlap 0.2
```
