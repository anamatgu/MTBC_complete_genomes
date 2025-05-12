
```
flye --pacbio-hifi $1 --out-dir "$SAMPLE".assembly.flye --genome-size 4.5m --threads 15 --iterations 2
```


```
circlator all --assembler canu {}.assembly.flye/assembly.fasta {}.filt.fastq.gz {}.circlator --genes_fa /data/ana_compartido/PACBIO/MTB_annotations/H37Rv_annot/H37Rv_dnaA.fa --threads 4
```



```
samtools faidx ASM.fasta

freebayes -f SAMPLE_ASM.fasta -m 0 --min-coverage 3 -R 0 -p 1 -F 0.1 -E -1 -b ASM_LRS.sort.bam --vcf SAMPLE.AF10.vcf

cat SAMPLE.AF10.vcf | vt normalize - -r SAMPLE.fasta -q > SAMPLE.vt.AF10.vcf; done
```

Indicate the path to vt in the script
```
python polishing.py SAMPLE.vt.AF10.vcf SAMPLE_ASM.fasta
```
