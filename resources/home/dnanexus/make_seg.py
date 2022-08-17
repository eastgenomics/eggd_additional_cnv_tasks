import pandas as pd
import argparse
from pysam import VariantFile


def read_vcf(vcf):
    """ Reads in vcf information into dataframe.

    Args:
        vcf (pysam object): Input vcf read through pysam

    Returns:
        df: dataframe of required information
    """

    # Create an empty dataframe
    df = pd.DataFrame(columns=["Sample","CHROM","POS","END","NP","CN"])

    for variant in vcf:


        assert len(list(variant.samples)) == 1, (
        "This app was created for single sample vcfs, "
        "can't work with multisample or the sample is missing.")

        # Get sample name from vcf
        sample=list(variant.samples)[0]

        # Grab information from the vcf and add to a Series
        entry = pd.DataFrame([{
            "Sample": sample.split('-')[0],
            "CHROM": variant.chrom,
            "POS": variant.start,
            "END": variant.stop,
            "CN":variant.samples[sample]['CN'],
            "NP":variant.samples[sample]['NP']
            }])

        # Add each Series to the dataframe
        df = pd.concat([df, entry], ignore_index=True, sort=False)

    return df


def main(args):

    patient=args.vcf

    # Read in the input patient vcf
    patient_vcf = VariantFile(patient)
    patient_vcf_basename = patient.split("/")[-1].rstrip(".vcf.gz")

    # Set output name
    output_seg = patient_vcf_basename + ".seg"

    # Parse vcf and output into a seg file
    seg = read_vcf(patient_vcf)
    seg.to_csv(output_seg, sep='\t', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf')

    args = parser.parse_args()

    main(args)