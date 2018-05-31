# 2M.1 FULLSTACKS - Implementation of TOPMed RNA-seq pipeline within Globus Genomics using FAIR principles

## Table of Contents
1. [Introduction](#introduction)
1. [Topmed RNAseq workflow](#topmed-rnaseq-workflow)
    1. [Summary](#summary)
    1. [Components](#components)
    1. [Reference Files](#reference-files)
1. [Integration of Minids and BDBags](#integration-of-minids-and-bdbags)
    1. [Get Data using MINID](#get-data-using-minid)
    1. [Publish Results using BDBag MINID](#publish-results-using-bdbag-and-minid)
    1. [Integrate BDBags/Minids with the Topmed RNAseq workflow](#integrate-bdbags-and-minids-with-topmed-rnaseq-workflow)
4. [End-to-end analysis using BDBags as inputs](#end---to---end-analysis-using-bdbags-as-inputs)
    1. [Authentication and Authorization](#authentication-and-authorization)
    1. [Using Python API](#using-python-api)
    1. [Using Globus Genomics Web UI](#using-globus-genomics-web-ui)
5. [List of BDBags](#list-of-bdbags)
    1. [Input Data](#input-data)
    1. [Outputs, Provenance and Performance](#outputs-provenance-and-performance)
    1. [Workflow, Tools and Tool wrappers](#workflow-tools-and-tool-wrappers)
    1. [Tools reference databases](#tools-reference-databases)

## Introduction
This README describes the implementation of TOPMed RNAseq analysis pipeline that uses BDBags and MINID within a Galaxy based Globus Genomics (GG) platform to support FAIR (Findable, Accessible, Interoperable, Reusable) research. We have implemented specific tools within GG that automate the use of MINIDs representing input databags and generate output BDBags along with provenance and performance metric that can be used to validate reproducibility.

## Topmed RNAseq workflow
We selected the TOPMed RNAseq pipeline as described in detail at: https://github.com/broadinstitute/gtex-pipeline/blob/master/TOPMed_RNAseq_pipeline.md
### Summary
For each input sample, this RNAseq pipeline generates:
1. Aligned RNAseq reads (BAM format)
2. QC Metrics on the aligned reads
3. Gene-level expression quantifications based on a collapsed version of a reference transcript annotation, provided as read counts and TPM.
4. Transcript-level expression quantifications, provided as TPM, expected read counts, and isoform percentages

### Components
The figure below describes the RNAseq pipeline and its components:
![Screenshot](images/TOPMed-RNAseq-pipeline.png)

We have wrapped the following versions of tools within Globus Genomics - Galaxy and we have made all the wrappers available within the [Tools BDBag](#workflow-tools-and-tool-wrappers) with MINID: [ark:/57799/b9t690](http://minid.bd2k.org/minid/landingpage/ark:/57799/b9t690)

The pipeline uses the following individul tools:
* Alignment: [STAR 2.5.3a](https://github.com/alexdobin/STAR/releases/tag/2.5.3a)
  * Post-processing: [Picard 2.9.0](https://github.com/broadinstitute/picard) [MarkDuplicates](https://broadinstitute.github.io/picard/command-line-overview.html#MarkDuplicates)
* Gene quantification and quality control: [RNA-SeQC 1.1.9](https://github.com/francois-a/rnaseqc)
* Transcript quantification: [RSEM 1.3.0](https://deweylab.github.io/RSEM/)
* Utilities: [SAMtools 1.6](https://github.com/samtools/samtools/releases) and [HTSlib 1.6](https://github.com/samtools/htslib/releases)

### Reference files
The tools listed above require Reference genomes. Following GRCh38 reference genome are used currently. We have created a [References BDBag](#tools-reference-databases) with all the reference databases in it. It can be accessed using the MINID: [ark:/57799/b9ph5b](http://minid.bd2k.org/minid/landingpage/ark:/57799/b9ph5b).

* Reference genome for RNA-seq alignment using STAR (contains .fasta, .fai, and .dict files): [Homo_sapiens_assembly38_noALT_noHLA_noDecoy_ERCC.tar.gz](https://personal.broadinstitute.org/francois/topmed/Homo_sapiens_assembly38_noALT_noHLA_noDecoy_ERCC.tar.gz)
* Collapsed gene model GTF: [gencode.v26.GRCh38.ERCC.genes.gtf.gz](https://personal.broadinstitute.org/francois/topmed/gencode.v26.GRCh38.ERCC.genes.gtf.gz)
* STAR index database: [STAR_genome_GRCh38_noALT_noHLA_noDecoy_ERCC_v26_oh100.tar.gz](https://personal.broadinstitute.org/francois/topmed/STAR_genome_GRCh38_noALT_noHLA_noDecoy_ERCC_v26_oh100.tar.gz)
* RSEM reference database: [rsem_reference_GRCh38_gencode26_ercc.tar.gz](https://personal.broadinstitute.org/francois/topmed/rsem_reference_GRCh38_gencode26_ercc.tar.gz)

## Integration of MINIDs and BDBags
We have added new tools within Globus Genomics to support the use of MINIDs and BDBags. We have specifically added two tools - 1) Get BDBag using MINID, and 2) Create BDBag and MINID 
### Get BDBag using MINID
Get BDBag using MINID is a new Galaxy tool we have added to GG that downloads all the data within the BDBag and adds it to Galaxy history. The following figure shows the tool withn GG.
![Screenshot](images/Get-BDBag-using-MINID.png)

### Publish results using BDBag and MINID
Create BDBag and MINID is a tool takes any history items or outputs of the tools and creates a BDBag and publishes it. It returns a MINID referencing the BDBag created. The following figure shows the tool within GG.

![Screenshot](images/Create-BDBag-and-Minid.png)

### Integrate BDBags and Minids with Topmed RNAseq workflow
In order to provide an end-to-end automation of running the TOPMed RNAseq pipeline by using a MINID as input, we integrated the two tools within the RNAseq workflow shown above in [Section 2/Components](#components). The resulting workflow is shown below:
![Screenshot](images/Get-and-create-integrated.png)

"Get BDBag using MINID" transfers all the data referenced by the MINID and feeds it into the first tool of the pipeline for analysis. 

And the last step in the pipline, "Create BDBag and MINID" takes the outputs of the workflow that are marked (orange stars in the above screenshot) and creates a new BDBag and generates a MINID for the bag. In addition to capturing the outputs of the analysis, this tools also collects provenance data in the form of actual command-lines with arguments that were used to run the tools, and performance metrics in the form of times taken to run the tools, and adds them to the new BDBag it creats. And example of the output BDBag is provided below under [section 5(ii).](#outputs-provenance-and-performance)

## End-to-end analysis using BDBags as inputs
### Authentication and Authorization
### Using Python API
### Using Globus Genomics Web UI

## List of BDBags
### Input Data
### Outputs, Provenance and Performance
### Workflow, Tools and Tool wrappers
### Tools reference databases
