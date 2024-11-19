#!/bin/bash
#SBATCH --partition=day
#SBATCH --time=23:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=102400

apptainer exec --bind $(pwd):/home cosi.sif /bin/bash <<EOF

# Function to run the command and check for success
run_command() {
    local output_name=\$1
    local sim_id=\$2
    local success=0

    while [ \$success -eq 0 ]; do
        # Generate a random number from an exponential distribution with a mean of 20
        local x=\$(awk -v mean=20 'BEGIN{srand(); print -mean*log(1-rand())}')
        # Calculate the probability density value for the generated x
        local s=\$(awk -v x=\$x -v mean=20 'BEGIN{print (1/mean) * exp(-x/mean)}')

        # Append the line to ../sel.demo.par
        echo "pop_event sweep_mult_standing \"sweep\" 1 U(0, 4000) \${s} .5 .05-.95 1 U(0, 4000)" >> ../sel.demo.par

        # Run the command in the background
        env COSI_NEWSIM=1 COSI_MAXATTEMPTS=1000000 coalescent -p ../sel.demo.par -v -g --genmapRandomRegions --drop-singletons .25 --tped \${output_name} -n 1 -M -m -r 0 &
        local cmd_pid=\$!

        # Wait for the command to finish or timeout after 1 minutes
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
            # Save the sim_id and s to a file
            echo "\${sim_id} \${s}" >> s_values.txt
        else
            echo "Run failed for \${output_name}, retrying..."
        fi

        # Remove the appended line from ../sel.demo.par
        sed -i '$ d' ../sel.demo.par
    done
}

# Loop to run the command for each output name from hap.0 to hap.1000
for a in \$(seq 0 999); do
    output_name="hap.\$a"
    run_command \$output_name \$a
done

EOF
