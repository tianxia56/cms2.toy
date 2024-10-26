import pandas as pd
import sys

def compute_delta_ihh(sim_id):
    input_file = f'{sim_id}.ihs.out'
    
    # Define the column names manually
    columns = [
        'locus', 'phys_pos', '1_freq', 'ihh_1', 'ihh_0', 'ihs',
        'derived_ihh_left', 'derived_ihh_right', 'ancestral_ihh_left', 'ancestral_ihh_right'
    ]
    
    # Read the selscan output file with the defined column names
    df = pd.read_csv(input_file, sep='\\s+', header=None, names=columns)
    
    # Compute derived and ancestral iHH
    df['derived_ihh'] = df['derived_ihh_left'] + df['derived_ihh_right']
    df['ancestral_ihh'] = df['ancestral_ihh_left'] + df['ancestral_ihh_right']
    
    # Compute ΔiHH
    df['delihh'] = df['derived_ihh'] - df['ancestral_ihh']
    
    # Select only the required columns for output
    output_df = df[['locus', 'phys_pos', 'ihs', 'delihh']]
    
    return output_df

def merge_selscan_outputs(sim_id):
    # Read the ihs output file
    ihs_file = f'{sim_id}.ihs.out'
    ihs_columns = [
        'locus', 'phys_pos', '1_freq', 'ihh_1', 'ihh_0', 'ihs',
        'derived_ihh_left', 'derived_ihh_right', 'ancestral_ihh_left', 'ancestral_ihh_right'
    ]
    ihs_df = pd.read_csv(ihs_file, sep='\\s+', header=None, names=ihs_columns)
    
    # Compute derived and ancestral iHH
    ihs_df['derived_ihh'] = ihs_df['derived_ihh_left'] + ihs_df['derived_ihh_right']
    ihs_df['ancestral_ihh'] = ihs_df['ancestral_ihh_left'] + ihs_df['ancestral_ihh_right']
    
    # Compute ΔiHH
    ihs_df['delihh'] = ihs_df['derived_ihh'] - ihs_df['ancestral_ihh']
    
    # Read the nsl output file
    nsl_file = f'{sim_id}.nsl.out'
    nsl_columns = ['locus', 'phys_pos', '1_freq', 'nsl1', 'nsl0', 'nsl']
    nsl_df = pd.read_csv(nsl_file, sep='\\s+', header=None, names=nsl_columns)
    
    # Read the ihh12 output file
    ihh12_file = f'{sim_id}.ihh12.out'
    ihh12_columns = ['locus', 'phys_pos', '1_freq', 'ihh12']
    ihh12_df = pd.read_csv(ihh12_file, sep='\\s+', header=0, names=ihh12_columns)
    
    # Read the xpehh output file
    xpehh_file = f'{sim_id}_1_vs_2.xpehh.out'
    xpehh_columns = ['locus', 'phys_pos', 'gpos', 'p1_freq', 'p1_ihh', 'p2_freq', 'p2_ihh', 'xpehh']
    xpehh_df = pd.read_csv(xpehh_file, sep='\\s+', header=0, names=xpehh_columns)
    
    # Merge all dataframes on locus and phys_pos
    merged_df = pd.merge(ihs_df[['locus', 'phys_pos', 'ihs', 'delihh']], nsl_df[['locus', 'phys_pos', 'nsl']], on=['locus', 'phys_pos'], how='outer')
    merged_df = pd.merge(merged_df, ihh12_df[['locus', 'phys_pos', 'ihh12']], on=['locus', 'phys_pos'], how='outer')
    merged_df = pd.merge(merged_df, xpehh_df[['locus', 'phys_pos', 'xpehh']], on=['locus', 'phys_pos'], how='outer')
    
    # Add sim.id column
    merged_df['sim.id'] = sim_id
    
    # Rename columns for final output
    merged_df.rename(columns={'phys_pos': 'pos'}, inplace=True)
    
    return merged_df

def merge_additional_outputs(sim_id):
    # Read the fst output file
    fst_file = f'{sim_id}_fst_1_vs_2.tsv'
    fst_columns = ['sim.id', 'pos', 'Fst']
    fst_df = pd.read_csv(fst_file, sep='\t')
    
    # Read the daf output file
    daf_file = f'{sim_id}_daf_1_vs_2.tsv'
    daf_columns = ['sim.id', 'pos', 'MAF', 'derFreq', 'delDAF']
    daf_df = pd.read_csv(daf_file, sep='\t')
    
    return fst_df, daf_df

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mk-delihh.py <sim.id>")
        sys.exit(1)
    
    sim_id = sys.argv[1]
    
    delta_ihh_df = compute_delta_ihh(sim_id)
    selscan_output_df = merge_selscan_outputs(sim_id)
    
    fst_df, daf_df = merge_additional_outputs(sim_id)
    
    # Merge all dataframes on sim.id and pos
    final_output_df = pd.merge(fst_df, daf_df, on=['sim.id', 'pos'], how='outer')
    final_output_df = pd.merge(final_output_df, selscan_output_df, on=['sim.id', 'pos'], how='outer')
    
    # Adjust the column order as specified
    final_output_columns_ordered = ['sim.id', 'pos', 'MAF', 'derFreq', 'delDAF', 'Fst', 'ihs', 'nsl', 'ihh12', 'xpehh', 'delihh']
    final_output_df = final_output_df[final_output_columns_ordered]
    
    final_output_file = f'{sim_id}_merged_components.tsv'
    final_output_df.to_csv(final_output_file, sep='\t', index=False)
    
    print(f"Merged selscan outputs have been saved to {final_output_file}.")
