import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python mk-selscans.py <sim.id> <pop1> <pop2>")
        sys.exit(1)
    
    sim_id = sys.argv[1]
    pop1 = int(sys.argv[2])
    pop2 = int(sys.argv[3])
    
    tped_file1 = f"{sim_id}_0_{pop1}.tped"
    tped_file2 = f"{sim_id}_0_{pop2}.tped"
    
    # Run selscan commands
    os.system(f"selscan --ihs --ihs-detail --tped {tped_file1} --out {sim_id} --threads 4")
    os.system(f"selscan --nsl --tped {tped_file1} --out {sim_id} --threads 4")
    os.system(f"selscan --ihh12 --tped {tped_file1} --out {sim_id} --threads 4")
    os.system(f"selscan --xpehh --tped {tped_file1} --tped-ref {tped_file2} --out {sim_id}_{pop1}_vs_{pop2} --threads 4")
    
    print("Selscan commands have been executed.")
