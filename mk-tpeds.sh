#!/bin/bash

# Function to run the command and check for success
run_command() {
    local output_name=$1
    local success=0

    while [ $success -eq 0 ]; do
        # Run the command in the background
        env COSI_NEWSIM=1 COSI_MAXATTEMPTS=1000000 coalescent -p sel.demo.par -v -g --genmapRandomRegions --drop-singletons .25 --tped ${output_name} -n 1 -M -m -r 0 &
        local cmd_pid=$!

        # Wait for the command to finish or timeout after 5 minutes
        local timeout=300
        local elapsed=0
        while kill -0 $cmd_pid 2>/dev/null; do
            sleep 1
            elapsed=$((elapsed + 1))
            if [ $elapsed -ge $timeout ]; then
                echo "Command running too long, killing process..."
                kill -9 $cmd_pid
                break
            fi
        done

        # Check if the command succeeded
        if wait $cmd_pid; then
            success=1
        else
            echo "Run failed for ${output_name}, retrying..."
        fi
    done
}

# Loop to run the command for each output name from hap.0000 to hap.1000
for a in $(seq 0 1000); do
    output_name=$(printf "hap.%04d" $a)
    run_command $output_name
done

# Restart the loop from the last sequence if needed
for a in $(seq $((a + 1)) 1000); do
    output_name=$(printf "hap.%04d" $a)
    run_command $output_name
done
