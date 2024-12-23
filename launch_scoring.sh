#!/bin/bash
#SBATCH --partition=week
#SBATCH --time=7-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=51200

# Load any necessary modules
module load your_module

# Navigate to the directory where your job will run
cd /home/tx56/palmer_scratch/cosi-sim

# Loop through sim.id values from hap.0513 to hap.1000
for i in $(seq -w 512 2500)
do
    sim_id=$(printf "hap.%04d" $i)
    python make-all-scores.py $sim_id 1 2
done
