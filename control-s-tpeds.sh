#!/bin/bash
#SBATCH --partition=week
#SBATCH --time=7-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=102400

apptainer exec --bind $(pwd):/home cosi.sif /bin/bash <<EOF

run_command() {
    local output_name=\$1
    local sim_id=\$2
    local success=0

    while [ \$success -eq 0 ]; do
        # Generate a random number between 0 and 5000
        local rand=\$((RANDOM % 5001))

        # Generate a random value for s between 0 and 0.5
        local s=\$(awk 'BEGIN{srand(); print rand() * 0.5}')

        # Make a copy of the .par file
        cp ../jv_nulldefault_constantsize.par ../jv_nulldefault_constantsize-\$sim_id.par

        # Add the one line command to the copied .par file
        echo "pop_event sweep_mult_standing \"sweep\" 1 U(0, \$rand) \${s} .5 .05-.95 1 U(0, \$rand)" >> ../jv_nulldefault_constantsize-\$sim_id.par

        # Run the command in the background
        env COSI_NEWSIM=1 COSI_MAXATTEMPTS=1000000 coalescent -p ../jv_nulldefault_constantsize-\$sim_id.par -v -g --genmapRandomRegions --drop-singletons .25 --tped \${output_name} -n 1 -M -m -r 0 &
        local cmd_pid=\$!

        # Wait for the command to finish or timeout after 1 minute
        local timeout=60
        local elapsed=0
        while kill -0 \$cmd_pid 2>/dev/null; do
            sleep 1
            elapsed=\$((elapsed + 1))
            if [ \$elapsed -ge \$timeout ]; then
                echo "Command running too long, killing process..."
                kill -9 \$cmd_pid
                break
            fi
        done

        # Check if the command succeeded
        if wait \$cmd_pid; then
            success=1
            # Save the sim_id, s, and rand to a file
            echo "\${sim_id} \${s} \${rand}" >> s_values_0k.txt
        else
            echo "Run failed for \${output_name}, retrying..."
        fi

        # Remove the copied .par file
        rm ../jv_nulldefault_constantsize-\$sim_id.par
    done
}

# Loop to run the command for each output name from hap.0 to hap.1000
for a in \$(seq 0 999); do
    output_name="hap.\$a"
    run_command \$output_name \$a
done

EOF
