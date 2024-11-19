#!/bin/bash

# Read the sorted_s_values.txt file and store the IDs and second column in arrays
mapfile -t ids < <(awk -F'\t' '{print $1}' sorted_s_values.txt)
mapfile -t s_values < <(awk -F'\t' '{print $2}' sorted_s_values.txt)

# Initialize an empty array to store the ratios
ratios=()

# Loop through each ID
for id in "${ids[@]}"; do
    # Construct the filename
    filename="hap.${id}_0_1.tped"
    
    # Initialize the ratio as "NA" in case the file or row is not found
    ratio="NA"
    
    # Check if the file exists
    if [[ -f "$filename" ]]; then
        # Extract the rows where the 4th column equals 1500000 and compute the ratio of 1s
        ratio=$(awk '$4 == 1500000 {
            total = 0;
            count_ones = 0;
            for (i = 5; i <= NF; i++) {
                total++;
                if ($i == 1) count_ones++;
            }
            ratio = count_ones / total;
            print ratio;
        }' "$filename")
    fi
    
    # Append the ratio to the ratios array
    ratios+=("$ratio")
done

# Create the new file with the header
echo -e "hap.id\ts\tderFreq" > hap-derf-plot.txt

# Loop through the arrays and write the combined data to the new file
for i in "${!ids[@]}"; do
    echo -e "${ids[$i]}\t${s_values[$i]}\t${ratios[$i]}" >> hap-derf-plot.txt
done
