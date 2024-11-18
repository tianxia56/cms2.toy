import subprocess
import pandas as pd
import os
import random

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def process_file(input_file, output_file):
    with open(input_file, 'r') as file, open(output_file, 'w') as new_file:
        for line in file:
            columns = line.split()[3:]
            if is_numeric(columns[0]):
                columns[0] = str(int(float(columns[0])))
            new_file.write('\t'.join(columns) + '\n')

def extract_10_percent_pairs(tped_file):
    with open(tped_file, 'r') as file:
        lines = file.readlines()

    selected_columns = []
    for line in lines:
        columns = line.split()[4:]  # Remove the first four columns
        pairs = [columns[i:i+2] for i in range(0, len(columns), 2)]  # Create pairs
        num_pairs = len(pairs)
        num_to_select = max(1, int(0.1 * num_pairs))  # Select 10% of the pairs, at least one pair
        selected_pairs = random.sample(pairs, num_to_select)
        selected_columns.append([item for sublist in selected_pairs for item in sublist])

    return selected_columns

def add_extra_columns(hap_file, tped_file):
    # Extract 10% of paired columns from the second .tped file
    extra_columns = extract_10_percent_pairs(tped_file)

    # Read the original hap file and append the extra columns to each line
    hap_df = pd.read_csv(hap_file, sep='\t', header=None)
    extra_columns_df = pd.DataFrame(extra_columns)
    # Concatenate the original hap file with the extra columns
    combined_df = pd.concat([hap_df, extra_columns_df], axis=1)
    
    # Save the combined dataframe to the hap file
    combined_df.to_csv(hap_file, sep='\t', header=False, index=False)

def run_isafe(input_file, output_prefix):
    command = f"isafe --input {input_file} --output {output_prefix} --format hap"
    subprocess.run(command, shell=True)

def add_isafe_to_components(sim_id):
    isafe_output_file = f"{sim_id}.iSAFE.out"
    components_file = f"./normed_scores_take1/{sim_id}_normed_components.tsv"

    if not os.path.exists(components_file):
        print(f"Skipping {sim_id} as {components_file} does not exist.")
        return

    isafe_df = pd.read_csv(isafe_output_file, sep='\t')
    components_df = pd.read_csv(components_file, sep='\t')

    merged_df = pd.merge(components_df, isafe_df[['POS', 'iSAFE']], left_on='pos', right_on='POS', how='left')
    merged_df.drop(columns=['POS'], inplace=True)

    # Save the merged data to a file named {sim_id}_merged_all_components.tsv
    merged_df.to_csv(f"{sim_id}_merged_all_components.tsv", sep='\t', index=False)

def main():
    for i in range(5001):
        sim_id = f"hap.{i:04d}"
        input_file_1 = f"{sim_id}_0_1.tped"
        input_file_2 = f"{sim_id}_0_2.tped"
        output_hap_file = f"{sim_id}.hap"

        if not os.path.exists(input_file_1) or not os.path.exists(input_file_2):
            print(f"Skipping {sim_id} as input files are missing.")
            continue

        # Process .tped file into .hap format
        process_file(input_file_1, output_hap_file)
        # Add extra columns to the .hap file
        add_extra_columns(output_hap_file, input_file_2)
        # Run iSAFE tool
        run_isafe(output_hap_file, sim_id)

        # Add iSAFE results to components and save the merged file
        add_isafe_to_components(sim_id)

        # Clean up intermediate files
        os.remove(output_hap_file)
        os.remove(f"{sim_id}.iSAFE.out")

if __name__ == "__main__":
    main()
