"""
Reads in vcf and calculates CNVLEN field

Args:
    - vcf to add length to
"""

import argparse
from pathlib import Path

from pysam import VariantFile


def add_length(vcf, output_name):
    """ Calculates length and adds it as a field to a new vcf

    Args:
        vcf (file): CNV VCF file containing END field.
        output_name (string): Name of output vcf
    """

    # Adds new field information in the vcf header
    vcf.header.add_meta('INFO', items=[
        ('ID', "CNVLEN"), ('Number', "1"), ('Type', 'Integer'),
        ('Description', 'Difference between END and POS coordinates')])

    # Create a new VCF object to write to with the above header
    out_vcf = VariantFile(output_name, 'w', header=vcf.header)

    for variant in vcf:
        # For each variant in the vcf calculate the length
        # variant.rlen = (END - POS) + 1  is a pysam built in function
        # Accounts for 1-base of the vcf
        variant.info.__setitem__('CNVLEN', variant.rlen)
        out_vcf.write(variant)

        print(
            f'Added record length CHROM {variant.chrom} ,'
            f'POS {variant.pos} END {variant.stop},'
            f'calculated length {variant.rlen} bp')

    out_vcf.close()


def main(args):

    patient = args.vcf

    # Read in the input patient vcf
    patient_vcf = VariantFile(patient)

    suffixes = "".join(Path(patient).suffixes)
    out_name = f'{Path(patient).name.replace(suffixes, "_length.vcf.gz")}'

    # Add length to vcf
    add_length(patient_vcf, out_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--vcf',
        help='Required single-sample input vcf containing END INFO field')

    args = parser.parse_args()

    main(args)
