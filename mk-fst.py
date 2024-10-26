import pandas as pd
import sys

def read_tped_file(filename):
    """Read TPED file and return a DataFrame."""
    columns = ['chromosome', 'snp_id', 'genetic_distance', 'position']
    df = pd.read_csv(filename, sep='\\s+', header=None, names=columns + list(range(4, 4 + (pd.read_csv(filename, sep='\\s+', nrows=1).shape[1] - 4))))
    return df

def compute_allele_frequencies(tped_df):
    """Compute allele frequencies for each SNP."""
    allele_counts = tped_df.iloc[:, 4:].apply(pd.Series.value_counts, axis=1).fillna(0)
    total_alleles = tped_df.iloc[:, 4:].shape[1]
    allele_frequencies = allele_counts / total_alleles
    return allele_frequencies

def compute_fst(tped_file1, tped_file2):
    """Compute FST between two populations."""
    tped_df1 = read_tped_file(tped_file1)
    tped_df2 = read_tped_file(tped_file2)
    
    af1 = compute_allele_frequencies(tped_df1)
    af2 = compute_allele_frequencies(tped_df2)
    
    # Calculate mean allele frequencies
    mean_af = (af1 + af2) / 2
    
    # Calculate FST
    num = (af1 - af2) ** 2
    denom = mean_af * (1 - mean_af)
    
    fst = (num.sum(axis=1) / denom.sum(axis=1)).round(4)
    
    result_df = pd.DataFrame({
        'sim.id': sim_id,
        'pos': tped_df1['position'],
        'Fst': fst
    })
    
    return result_df

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python mk-fst.py <sim.id> <pop1> <pop2>")
        sys.exit(1)
    
    sim_id = sys.argv[1]
    pop1 = int(sys.argv[2])
    pop2 = int(sys.argv[3])
    
    tped_file1 = f"{sim_id}_0_{pop1}.tped"
    tped_file2 = f"{sim_id}_0_{pop2}.tped"
    
    fst_df = compute_fst(tped_file1, tped_file2)
    
    output_file = f"{sim_id}_fst_{pop1}_vs_{pop2}.tsv"
    fst_df.to_csv(output_file, sep='\t', index=False)
    
    print(f"FST values have been computed and saved to {output_file}.")
