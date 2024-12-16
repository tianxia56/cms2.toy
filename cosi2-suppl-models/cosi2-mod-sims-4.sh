#!/bin/bash
#SBATCH --partition=day
#SBATCH --time=23:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=102400

apptainer exec --bind $(pwd):/home cosi.sif /bin/bash <<EOF

run_command() {
    local output_name=\$1
    local sim_id=\$2
    local add_line=\$3
    local success=0

    while [ \$success -eq 0 ]; do

        # Make a copy of the .par file
        cp ../model4.par ../model4-\$sim_id.par

        # Conditionally add the extra line to the copied .par file
        if [ "\$add_line" -eq 1 ]; then
            echo "pop_event sweep \"sweep\" 1 U(0, 2000) .0185 .5 .8 1 U(0, 2000)" >> ../model4-\$sim_id.par
        fi

        # Run the command in the background
        env COSI_NEWSIM=1 COSI_MAXATTEMPTS=1000000 coalescent -p ../model4-\$sim_id.par -v -g --tped \${output_name} -n 1 -M -m -r 0 &
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
        fi

        # Remove the copied .par file
        rm ../model4-\$sim_id.par
    done
}

# Loop to run the command for each output name from hap.neut.0 to hap.neut.99 without the extra line
for a in \$(seq 0 99); do
    output_name="mod4.hap.neut.\$a"
    run_command \$output_name \$a 0
done

# Loop to run the command for each output name from hap.sel.0 to hap.sel.99 with the extra line
for a in \$(seq 0 99); do
    output_name="mod4.hap.sel.\$a"
    run_command \$output_name \$a 1
done

EOF
