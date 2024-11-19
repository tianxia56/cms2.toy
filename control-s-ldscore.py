import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to compute LD r2 between two loci
def compute_ld_r2(genotypes1, genotypes2):
    # Convert genotypes to numpy arrays
    genotypes1 = np.array(genotypes1, dtype=int)
    genotypes2 = np.array(genotypes2, dtype=int)
    
    # Calculate allele frequencies
    p_A = np.mean(genotypes1 == 1)
    p_B = np.mean(genotypes2 == 1)
    
    # Calculate D'
    D = np.mean((genotypes1 == 1) & (genotypes2 == 1)) - (p_A * p_B)
    
    # Calculate r2, handle division by zero
    if p_A * (1 - p_A) * p_B * (1 - p_B) == 0:
        r2 = 0
    else:
        r2 = D**2 / (p_A * (1 - p_A) * p_B * (1 - p_B))
    
    return r2

# Load the data from hap-derf-plot.txt
data = pd.read_csv('hap-derf-plot.txt', sep='\t')

# Initialize a list to store the LD scores
ld_scores = []

# Iterate over ids from the first column of hap-derf-plot.txt
for id in data['hap.id']:
    sim_id = f"hap.{int(id)}_0_1"
    tped_file = f"{sim_id}.tped"
    
    # Open the tped file and read its content
    try:
        with open(tped_file, 'r') as file:
            lines = file.readlines()
        
        # Extract genotypes for the position where the 4th column is equal to 1500000
        target_genotypes = None
        other_genotypes = []

        for line in lines:
            columns = line.strip().split()
            if columns[3] == '1500000':
                # Extract genotypes from the 5th column to the end for the target position
                target_genotypes = columns[4:]
                # Convert pairs of genotypes to individual genotypes
                target_genotypes = [target_genotypes[i] for i in range(0, len(target_genotypes), 2)]
            else:
                # Extract genotypes from the 5th column to the end for other positions
                genotypes = columns[4:]
                # Convert pairs of genotypes to individual genotypes
                genotypes = [genotypes[i] for i in range(0, len(genotypes), 2)]
                other_genotypes.append(genotypes)

        # Compute the sum of all pairwise LD r2 values between pos=1500000 and other positions
        ld_r2_sum = 0
        if target_genotypes is not None:
            for genotypes in other_genotypes:
                ld_r2_sum += compute_ld_r2(target_genotypes, genotypes)
        
        ld_scores.append(ld_r2_sum)
    
    except FileNotFoundError:
        print(f"File {tped_file} not found.")
        ld_scores.append(None)

# Add the LD scores as a new column to the dataframe
data['ld_score'] = ld_scores

# Save the updated dataframe to a new file with header
data.to_csv('hap-derf-plot-updated.txt', sep='\t', index=False, header=True)

# Plot density of ld_score
plt.figure(figsize=(10, 6))
sns.kdeplot(data['ld_score'].dropna(), shade=True)
plt.xlabel('LD Score')
plt.ylabel('Density')
plt.title('Density Plot of LD Scores')
plt.grid(True)
plt.savefig('ld_scores_density_plot.png')
plt.show()

# Plot scatter x=s, y=ld_score
plt.figure(figsize=(10, 6))
plt.scatter(data['s'], data['ld_score'], color='b')
plt.xlabel('s')
plt.ylabel('LD Score')
plt.title('Scatter Plot of s vs LD Score')
plt.grid(True)
plt.savefig('s_vs_ld_score_scatter_plot.png')
plt.show()
