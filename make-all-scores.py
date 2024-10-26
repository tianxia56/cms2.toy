import os
import sys

def run_commands(sim_id, pop1, pop2):
    commands = [
        f"python mk-fst.py {sim_id} {pop1} {pop2}",
        f"python mk-freqs.py {sim_id} {pop1} {pop2}",
        f"python mk-selscans.py {sim_id} {pop1} {pop2}",
        f"python mk-delihh-merge.py {sim_id}"
    ]
    
    for command in commands:
        os.system(command)
    
    # Print completion messages
    print(f"FST values have been computed and saved to hap.{sim_id}_fst_{pop1}_vs_{pop2}.tsv.")
    print(f"Allele frequencies have been computed and saved to hap.{sim_id}_daf_{pop1}_vs_{pop2}.tsv.")
    print("Selscan commands have been executed.")
    print(f"Merged selscan outputs have been saved to hap.{sim_id}_merged_selscan.tsv.")
    
    # Remove the specified outputs
    outputs_to_remove = [
        f"{sim_id}_fst_{pop1}_vs_{pop2}.tsv",
        f"{sim_id}_daf_{pop1}_vs_{pop2}.tsv",
        f"{sim_id}.ihs.out",
        f"{sim_id}.ihs.log",
        f"{sim_id}.nsl.out",
        f"{sim_id}.nsl.log",
        f"{sim_id}.ihh12.out",
        f"{sim_id}.ihh12.log",
        f"{sim_id}_{pop1}_vs_{pop2}.xpehh.out",
        f"{sim_id}_{pop1}_vs_{pop2}.xpehh.log"
    ]
    
    for output in outputs_to_remove:
        try:
            os.remove(output)
            print(f"Removed file: {output}")
        except FileNotFoundError:
            print(f"File not found, could not remove: {output}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python make-all-scores.py <sim.id> <pop1> <pop2>")
    else:
        sim_id = sys.argv[1]
        pop1 = sys.argv[2]
        pop2 = sys.argv[3]
        run_commands(sim_id, pop1, pop2)
