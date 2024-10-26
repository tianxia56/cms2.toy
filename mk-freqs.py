import pandas as pd
import sys

def read_tped_file(filename):
    """Read TPED file and return a DataFrame."""
    columns = ['chromosome', 'snp_id', 'genetic_distance', 'position']
    df = pd.read_csv(filename, sep='\\s+', header=None, names=columns + list(range(4, 4 + (pd.read_csv(filename, sep='\\s+', nrows=1).shape[1] - 4))))
    return df

def compute_derived_allele_frequency(tped_df):
    """Compute derived allele frequency for each SNP."""
    derived_allele_counts = tped_df.iloc[:, 4:].sum(axis=1)
    total_alleles = tped_df.iloc[:, 4:].shape[1]
    derived_allele_frequency = (derived_allele_counts / total_alleles).round(4)
    return derived_allele_frequency

def compute_minor_allele_frequency(tped_df):
    """Compute minor allele frequency for each SNP."""
    allele_counts = tped_df.iloc[:, 4:].apply(pd.Series.value_counts, axis=1).fillna(0)
    minor_allele_frequency = (allele_counts.min(axis=1) / tped_df.iloc[:, 4:].shape[1]).round(4)
    return minor_allele_frequency

def compute_delta_derived_allele_frequency(tped_file1, tped_file2):
    """Compute delta derived allele frequency between two populations."""
    tped_df1 = read_tped_file(tped_file1)
    tped_df2 = read_tped_file(tped_file2)
    
    daf1 = compute_derived_allele_frequency(tped_df1)
    daf2 = compute_derived_allele_frequency(tped_df2)
    
    delta_daf = (daf1 - daf2).round(4)
    
    maf1 = compute_minor_allele_frequency(tped_df1)
    
    result_df = pd.DataFrame({
        'sim.id': sim_id,
        'pos': tped_df1['position'],
        'MAF': maf1,
        'derFreq': daf1,
        'delDAF': delta_daf
    })
    
    return result_df

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python mk-daf.py <sim.id> <pop1> <pop2>")
        sys.exit(1)
    
    sim_id = sys.argv[1]
    pop1 = int(sys.argv[2])
    pop2 = int(sys.argv[3])
    
    tped_file1 = f"{sim_id}_0_{pop1}.tped"
    tped_file2 = f"{sim_id}_0_{pop2}.tped"
    
    delta_daf_df = compute_delta_derived_allele_frequency(tped_file1, tped_file2)
    
    output_file = f"{sim_id}_daf_{pop1}_vs_{pop2}.tsv"
    delta_daf_df.to_csv(output_file, sep='\t', index=False)
    
    print(f"Allele frequencies have been computed and saved to {output_file}.")
