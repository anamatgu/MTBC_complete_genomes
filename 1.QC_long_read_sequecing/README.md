## Quality control of long reads and filtering



### Taxonomic filtering using Kraken and KrakenTools

[Kraken](https://ccb.jhu.edu/software/kraken/) (v1)

```
/Kraken/kraken --db /KrakenDB/KRefSeqHumanSARS/ --fastq-input  --output SAMPLE.kraken --threads 20 --gzip-compressed SAMPLE.fastq.gz

/Kraken/kraken-report --db /KrakenDB/KRefSeqHumanSARS/ SAMPLE.kraken > SAMPLE.kraken.report
```

If readso filter reads belonging to other species, the following script can be used:

```
python /KrakenTools-1.2/extract_kraken_reads.py -k SAMPLE.kraken -s SAMPLE.fastq.gz -o SAMPLE.filtered.fastq -t 77643 --fastq-output -r SAMPLE.kraken.report --include-children -r
```

### Adapter filtering using HiFiAdapterFilt

[HifiAdapterFilt](https://github.com/sheinasim-USDA/HiFiAdapterFilt)

```
bash /HiFiAdapterFilt-2.0.0/pbadapterfilt.sh -t 15
```

### Quality control

[LongQC](https://github.com/yfukasawa/LongQC)

```
python3 /LongQC/longQC.py sampleqc -x pb-rs2 -s SAMPLE -o SAMPLE_QC SAMPLE.fastq.gz
```

[pbmm2](https://github.com/PacificBiosciences/pbmm2)
```
pbmm2 align MTBCA_reference.fasta SAMPLE.fastq SAMPLE.sort.bam --preset CCS --sort --sample SAMPLE --rg '@RG\tID:mXXXXX\tSM:mysample'
```

### Mismatch rate

```
python mismatch_rate.py
```
