# eggd_additional_cnv_tasks
Adds CNV length value to vcf and creates visualisation seg file

## What does this app do?

Given a gCNV vcf input, it calculates and adds the event length to each variant.

It also creates a [seg file](https://software.broadinstitute.org/software/igv/SEG) to aid visualisation. Seg files are bed like files with additional numeric columns to give additional information while visualising in IGV.

## What are typical use cases for this app?
This app was designed to be used in the CNV reports workflow. It is meant to go after vcf annotation and before report creation.

It outputs a vcf with event length information as required for interpretation by the clinical scientists.

## What data are required for this app to run?
- An input vcf which contains a variant END variable (`vcf`)

## What are the optional inputs for this app?
- `length_only` - boolean flag to only output the edited vcf
- `seg_only` - boolean flag to only output the seg file


__This app uses the following tools which are app assets:__
* htslib (v1.14)


## What does this app output?
- VCF with added CNV length for each variant as additional INFO field
- Seg file for visualisation of events
  - This file contains the following columns:
    - **Sample** - Sample identifier.
    - **Chrom** - Chromosome
    - **Pos** - Position of event (1-based)
    - **End** - End coordinate of event
    - **NP** - Number of points (targets in CNV calling)
    - **CN** - copy number of event (colours bar in IGV depending on CN)

## Notes

Example seg file:
```
Sample	CHROM	POS	END	NP	CN
CEN20CNV	19	11238572	11238901	2	3
```