#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_dir>"
    exit 1
fi
input_dir="$1"
output_dir="output"
mkdir -p "$output_dir"

split_file() {
    input_file="$1"
    filename=$(basename "$input_file")
    prefix=$(echo "$filename" | cut -d'.' -f1-2)  # extracts '0.chr21.'

    # extract the header to determine the "POS" column index
    header=$(zcat < "$input_file" | head -1)
    pos_index=$(echo "$header" | tr '\t' '\n' | grep -n -w "POS" | cut -d: -f1)

    if [ -z "$pos_index" ]; then
        echo "Error: 'POS' column not found in $input_file."
        return 1
    fi

    chunk_size=1000000
    start=10000000
    for _ in {0..4}; do
        end=$((start + chunk_size - 1))
        output_file="${output_dir}/${prefix}.${start}_${end}.tsv"
        zcat < "$input_file" | awk -v pos_index="$pos_index" -v start="$start" -v end="$end" -F'\t' '
        BEGIN {OFS=FS}
        NR==1 || ($pos_index >= start && $pos_index <= end) {print}' > "$output_file"
        gzip "$output_file"
        start=$((end + 1))
    done
    echo "Split $input_file into 5 chunks."
}

# loop through all .tsv.gz files in the input directory and split each one into 5 smaller files, 1Mbp each
find "$input_dir" -type f -name "*.tsv.gz" | while read -r file; do
    split_file "$file"
done
echo "All files in $input_dir have been processed."
