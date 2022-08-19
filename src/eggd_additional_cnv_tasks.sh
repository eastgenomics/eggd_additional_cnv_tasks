#!/bin/bash
# eggd_additional_cnv_tasks 1.0.0
# Generated by dx-app-wizard.

# -e = exit on error; -x = output each line that is executed to log; -o pipefail = throw an error if there's an error in pipeline
set -e -x -o pipefail

main() {

    echo "Value of vcf: '$vcf'"
    echo "Value of length_only: '$output_length'"
    echo "Value of seg_only: '$output_seg'"

    # Download input vcf
    dx download "$vcf"


    mark-section "Installing packages"
    export PATH=$PATH:/home/dnanexus/.local/bin  # pip installs some packages here, add to path

    sudo -H python3 -m pip install --no-index --no-deps packages/*

    mkdir -p /home/dnanexus/out/seg_file
    mkdir -p /home/dnanexus/out/output_vcf

    outname=$(sed 's/.vcf\|.gz//g' <<< "$vcf_name")

    # Check if not compressed and compress
    if [[ $vcf_name == *vcf ]]; then
            bgzip $vcf_name
    fi

    # Check if both outputs have been turned off and exit
    if [ "$output_length" == false ] && [ "$output_seg" == false ]; then
       dx-jobutil-report-error "Invalid option combination, this will not output anything. :)"
       exit 1
    fi

    # Add length to vcf if required
    if [ "$output_length" == true ]; then

        mark-section "Adding length to CNV"

        bcftools index ${outname}.vcf.gz
        python3 /home/dnanexus/add_length.py --vcf ${outname}.vcf.gz

        mv "${outname}_length.vcf.gz" /home/dnanexus/out/output_vcf/
    fi

    # Create seg file if required
    if [ "$output_seg" == true ]; then

        mark-section "Making seg visualisation file"

        python3 /home/dnanexus/make_seg.py --vcf ${outname}.vcf.gz
        mv /home/dnanexus/${outname}.seg /home/dnanexus/out/seg_file/

    fi

    mark-section "Uploading output"
    # upload all outputs
    dx-upload-all-outputs --parallel

}
