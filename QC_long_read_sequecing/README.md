## Quality control of long reads and filtering




```
/Kraken/kraken --db /KrakenDB/KRefSeqHumanSARS/ --fastq-input  --output SAMPLE.kraken --threads 20 --gzip-compressed SAMPLE.fastq.gz
```

```
/Kraken/kraken-report --db /KrakenDB/KRefSeqHumanSARS/ SAMPLE.kraken > SAMPLE.kraken.report
```

```
python /KrakenTools-1.2/extract_kraken_reads.py -k SAMPLE.kraken -s SAMPLE.fastq.gz -o SAMPLE.filtered.fastq -t 77643 --fastq-output -r SAMPLE.kraken.report --include-children -r
```

```
python3 /LongQC/longQC.py sampleqc -x pb-rs2 -s SAMPLE -o SAMPLE_QC SAMPLE.fastq.gz
```
