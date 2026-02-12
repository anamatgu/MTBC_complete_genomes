# Analysis of MTBC complete genomes

This repository has been created to describe and reproduce the steps followed for analysing a dataset composed of 216 Mycobacterium tuberculosis complex (MTBC) complete genomes. The repository contains different directories with specific analyses and customized scripts that follow this order:

1. Filtering and quality control of long reads
2. _De novo_ assembly, polishing, and lift-over
4. Multiple Genome Alignment: construction, refinement, and variant calling


## Data availability

The MTBC long-read sequences and assemblies analyzed in this study have been deposited on the [European Nucleotide Archive](https://www.ebi.ac.uk/ena/browser/home) project PRJEB89421. An inferred MTBC most likely common ancestor (MTBCA) was used as the reference genome, and it can be found on https://doi.org/10.5281/zenodo.3497110

## System requirements

To ensure stable performance and reproducibility, this code has been rigorously tested on the Linux CentOS 7 operating system. Running the pipeline on other Linux distributions may require adjustments to environment variables or library paths. The workflow relies on a specific suite of bioinformatics tools and language runtimes; for optimal results, it is recommended to manage these via a dedicated Conda environment to avoid version conflicts.

The following dependencies are required:

- Python (v3.7)
- pbmm2 (v1.13)
- minimap2 (v2.26)
- samtools (v1.15)
- Flye (v2.9.2)
- Circlator (v1.5.5)
- LongQC (v1.2.0b)
- Kraken (v0.10.5)
- HifiAdapter (v2.0.0)
- Freebayes (v1.3.6)
- vt (v0.57721)
- Liftoff (v1.6.3)
- Minigraph-Cactus (v2.8.4)
- dnadiff (v1.3)

## Installation guide

We recommend using Conda or Mamba to manage the specific versions of Python and the bioinformatic dependencies required. This prevents conflicts with your system libraries. Once the base dependencies are installed, clone this repository and prepare the internal scripts:

Clone the Repo: git clone https://github.com/anamatgu/MTBC_complete_genomes.git cd MTBC_complete_genomes

Permissions: Ensure the custom Python scripts are executable: chmod +x scripts/*.py

Standard setup via Conda typically takes 15–30 minutes, depending on your internet connection and system hardware.

## Demo and Instruction for use

This pipeline is designed to process standard FASTQ files containing PacBio HiFi reads. The core workflow handles long-read data to perform assembly, quality control, and comparative genomic analysis.

Because this repository contains a modular collection of custom Python scripts and third-party bioinformatic tools, the specific execution steps are organized by analysis type. For detailed, step-by-step walkthroughs—including sample commands and parameter configurations—please refer to the README files located within the individual subdirectories:

1.QC_long_read_sequecing: Guidelines for read quality assessment and adapter removal.

2.De_novo_assembly_polishing: Instructions for genome assembly, circularization, polishing, and lift-over.

3.MGA: Procedures for Multiple Genome Alignment.

The expected runtime for a demo on a standard desktop computer varies significantly depending on the number of samples and the complexity of the specific analysis being performed.
