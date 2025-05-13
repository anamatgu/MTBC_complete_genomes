## Quality control of long reads and filtering
Before performing _de novo_ assembly, long reads were filtered by taxonomy and reads with HiFi adapters were removed. 


### Taxonomic filtering using Kraken and KrakenTools
Long reads were classified by taxonomy with [Kraken](https://ccb.jhu.edu/software/kraken/) (v1) 

```
/Kraken/kraken --db /KrakenDB/KRefSeqHumanSARS/ --fastq-input  --output SAMPLE.kraken --threads 20 --gzip-compressed SAMPLE.fastq.gz

/Kraken/kraken-report --db /KrakenDB/KRefSeqHumanSARS/ SAMPLE.kraken > SAMPLE.kraken.report
```

To keep only those reads belonging to the Mycobacterium tuberculosis complex, the following script from [KrakenTools](https://github.com/jenniferlu717/KrakenTools) can be used:

```
python /KrakenTools-1.2/extract_kraken_reads.py -k SAMPLE.kraken -s SAMPLE.fastq.gz -o SAMPLE.filtered.fastq -t 77643 --fastq-output -r SAMPLE.kraken.report --include-children -r
```

### Adapter filtering using HiFiAdapterFilt

CCS reads containing PacBio adapter sequences were removed with [HifiAdapterFilt](https://github.com/sheinasim-USDA/HiFiAdapterFilt) (v2)

```
bash /HiFiAdapterFilt-2.0.0/pbadapterfilt.sh -t 15
```

### Quality control

The basic statistics for long-read sequencing with PacBio Sequel II can be obtained using [LongQC](https://github.com/yfukasawa/LongQC) and the following parameters:

```
python3 /LongQC/longQC.py sampleqc -x pb-rs2 -s SAMPLE -o SAMPLE_QC SAMPLE.fastq.gz
```
Additionally, long reads were mapped against the MTBC ancestor reference genome using [pbmm2](https://github.com/PacificBiosciences/pbmm2) to determine the horizontal coverage and depth.

```
pbmm2 align MTBCA_reference.fasta SAMPLE.fastq SAMPLE.sort.bam --preset CCS --sort --sample SAMPLE --rg '@RG\tID:mXXXXX\tSM:mysample'
```

### Mismatch rate
To obtain the mismatch rate, the BAM files must be converted to SAM format with the =/X CIGAR. The following script will detect all SAM files in the directory:

```
python mismatch_rate.py
```
This script will output the following parameters in CSV format: 
