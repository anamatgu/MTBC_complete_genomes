## _De novo_ assembly and polishing

### _De novo_ assembly with Flye
Once the long reads were filtered, de novo assembly was performed with [Flye](https://github.com/mikolmogorov/Flye) (v2.9.2) with two polishing iterations:

```
flye --pacbio-hifi SAMPLE.fastq.gz --out-dir SAMPLE_ASM.flye --genome-size 4.5m --threads 15 --iterations 2
```


```
circlator all --assembler canu SAMPLE_ASM.fasta SAMPLE.fastq.gz SAMPLE_ASM.circlator --genes_fa H37Rv_dnaA.fa --threads 4
```


### Customized polishing with long reads

```
samtools faidx ASM.fasta



freebayes -f SAMPLE_ASM.fasta -m 0 --min-coverage 3 -R 0 -p 1 -F 0.1 -E -1 -b ASM_LRS.sort.bam --vcf SAMPLE.AF10.vcf

cat SAMPLE.AF10.vcf | vt normalize - -r SAMPLE.fasta -q > SAMPLE.vt.AF10.vcf; done
```

Indicate the path to vt in the script
```
python polishing.py SAMPLE.vt.AF10.vcf SAMPLE_ASM.fasta
```
